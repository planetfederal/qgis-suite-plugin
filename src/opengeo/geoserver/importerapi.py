import collections
import logging
import json
import os
import pprint

STATE_PENDING = "PENDING"
STATE_READY = "READY"
STATE_RUNNING = "RUNNING"
STATE_INCOMPLETE = "INCOMPLETE"
STATE_COMPLETE = "COMPLETE"

_logger = logging.getLogger("gsuploader")

class BadRequest(Exception):
    '''Encapsulate a 400 or other 'invalid' request'''
    pass

class RequestFailed(Exception):
    '''Encapsulate a 500 or other 'failed' request'''
    pass

class NotFound(Exception):
    '''Encapsulate an HTTP 404 or other 'missing' request'''
    pass

class BindingFailed(Exception):
    '''Something in the API has changed'''
    pass

def parse_response(args, parent=None):
    '''Parse a top-level concept from the provided args.
    :param args: a tuple of headers, response from an httplib2 request
    :param parent: if present, set the parent of any returned object
    :returns: a Session, Task or list of Session or Task
    '''
    headers, response = args    
    try:
        resp = json.loads(response)
    except ValueError,ex:
        _logger.warn('invalid JSON response: %s',response)
        raise ex       
    if "import" in resp:
        return Session(json=resp['import'], parent=parent)
    elif "task" in resp:
        return Task(resp['task'], parent=parent)
    elif "imports" in resp:
        return [ Session(json=j, parent=parent) for j in resp['imports'] ]
    elif "tasks" in resp:
        # non-recognized file tasks have null source.format
        return [ Task(t, parent=parent) for t in resp['tasks'] ]
    raise Exception("Unknown response %s" % resp)


_Binding = collections.namedtuple('Binding', [
        'name', 'expected', 'ro', 'binding'
    ])
def _binding(name, expected=True, ro=True, binding=None):
    return _Binding(name, expected, ro, binding)



class _UploadBase(object):
    _object_name = None

    def __init__(self, json, parent=None):
        self._parent = parent
        if parent == self:
            raise Exception('bogus')
        self._bind_json(json)
        self._vals = {}
        self._uploader = None

    def reload(self):
        '''reset the state of this object if possible'''
        if not hasattr(self, 'href'):
            raise Exception('cannot reload %s', type(self))
        resp = self._client()._request(self.href + "?expand=3")
        # if we have a parent, keep it, otherwise, we're the new parent
        parsed = parse_response(resp, parent=self._parent or self)
        for binding in self._bindings:
            setattr(self, binding.name, getattr(parsed, binding.name))
        return self

    def save(self, deep=False):
        raise Exception('not implemented')

    def _bind_json(self, json):        
        # generally, not required for override. instead use _bind_custom_json
        # if possible
        if not isinstance(json, dict):
            self._binding_failed('expected dict, got %s', type(json))
        for binding in self._bindings:
            val = json.pop(binding.name, None)
            if binding.expected and val is None:
                self._binding_failed('expected val for %s', binding.name)
            if binding.binding and val is not None:
                if isinstance(val, list):
                    val = [binding.binding(v, parent=self) for v in val]
                else:
                    val = binding.binding(val, parent=self)
            setattr(self, binding.name, val)
        self._bind_custom_json(json)

    def _bind_custom_json(self, json):
        # do any custom binding like for a shortcut
        pass

    def _binding_failed(self, msg, args):
        raise BindingFailed('[%s] %s' % (type(self), msg % args))

    def _getuploader(self):
        comp = self
        while comp:
            if comp._uploader:
                return comp._uploader
            comp = comp._parent

    def _url(self,spec,*parts):
        return self._getuploader().client.url( spec % parts )

    def _client(self):
        return self._getuploader().client

    def _to_json_object(self, deep=True, top_level=True):
        json = {}
        for binding in self._bindings:
            val = getattr(self, binding.name, None)
            if isinstance(val, _UploadBase):
                val = val._to_json_object(top_level=False)
            if val is not None:
                json[binding.name] = val
        self._to_json_object_custom(json)
        if top_level and self._object_name:
            json = { self._object_name : json }
        return json

    def _to_json_object_custom(self, json):
        pass

    def __repr__(self):
        jsonobj = self._to_json_object(deep=True)
        return pprint.pformat(jsonobj, indent=4)


class Data(_UploadBase):
    _object_name = 'data'
    _bindings = (
        _binding('type'),
        # a missing format indicates an undetected format
        _binding('format', expected=False),
        _binding('charset', expected=False),
        # either file or files...
        _binding('file', expected=False),
        _binding('files', expected=False),
    )


class Target(_UploadBase):
    '''This is basically a StoreInfo'''
    _object_name = 'target'
    _bindings = (
        _binding('name'),
        _binding('type'),
        _binding('enabled'),
    )

    # this allows compatibility with the gsconfig datastore object
    resource_type = "featureType"

    def _bind_json(self, json):
        self.href = json.get('href')
        repr = [ json[k] for k in ('dataStore', 'coverageStore', 'store') if k in json]
        if len(repr) != 1:
            self._binding_failed('invalid store entry: %s', json.keys())
        super(Target, self)._bind_json(repr[0])

    def _bind_custom_json(self, json):
        workspace = json.get('workspace', None)
        if workspace:
            self.workspace_name = workspace['name']

    def change_datastore(self, store_name, workspace=None):
        '''Immediately change the target to the specified datastore. The workspace
        must exist prior to setting as the target.

        :param store_name: An existing datastore name
        :param workspace: An optional workspace to use for referencing the store
        '''
        dataStore = { 'name' : store_name }
        if workspace:
            dataStore['workspace'] = { 'name' : str(workspace) }
        target_rep = { 'dataStore' : dataStore }
        self._client().put_json(self.href,json.dumps(target_rep))


class BBox(_UploadBase):
    _bindings = (
        _binding('minx'),
        _binding('miny'),
        _binding('maxx'),
        _binding('maxy'),
        _binding('crs'),
    )


class Attribute(_UploadBase):
    _bindings = (
        _binding('name'),
        _binding('binding')
    )


class Layer(_UploadBase):
    _object_name = 'layer'
    _bindings = (
        _binding('name'),
        _binding('href'),
        _binding('originalName'),
        _binding('nativeName'),
        _binding('srs'),
        _binding('bbox', binding=BBox),
    )

    def set_target_layer_name(self, name):
        data = { 'layer' : { 'name' : name }}
        self._client().put_json(self.href, json.dumps(data))


class Task(_UploadBase):
    _object_name = 'task'
    _bindings = (
        _binding('id'),
        _binding('href'),
        _binding('state'),
        #_binding('progress'),
        #_binding('updateMode'),
        #_binding('data', binding=Data),
        _binding('target', binding=Target),
        # a missing layer probably indicates an undetected format
        _binding('layer', binding=Layer, expected=False),
    )

    def _bind_custom_json(self, json):
        self.transform_type = json['transformChain']['type']
        self.transforms = json['transformChain']['transforms']

    # Convience methods
    def get_target_layer_name(self):
        '''Get the workspace prefixed target layer name.
        For example: `topp:world_borders`
        '''
        return '%s:%s' % (self.target.workspace_name, self.layer.name)

    # Mutators
    def set_target(self, store_name, workspace):
        data = { 'task' : {
            'target' : {
                'dataStore' : {
                    'name' : store_name,
                    'workspace' : {
                        'name' : workspace
                    }
                }
            }
        }}
        self._client().put_json(self.href, json.dumps(data))

    def set_update_mode(self,update_mode):
        data = { 'task' : {
            'updateMode' : update_mode
        }}
        self._client().put_json(self.href,json.dumps(data))

    def set_charset(self,charset):
        data = { 'task' : {
            'source' : {
                'charset' : charset
            }
        }}
        self._client().put_json(self.href,json.dumps(data))

    def delete(self):
        """Delete the task"""
        resp, content = self._client().delete(self.href)
        if resp['status'] != '204':
            raise Exception('expected 204 response code, got %s' % resp['status'],content)

    def set_transforms(self, transforms):
        """Set the transforms of this Item. transforms is a list of dicts"""
        self.transforms = list(transforms)
        chain = {
            "type": self.transform_type,
            "transforms": self.transforms
        }
        data = { 'task' : { 'transformChain' : chain}}
        self._client().put_json(self.href, json.dumps(data))

    def add_transforms(self, transforms):
        self.transforms.extend(transforms)
        self.set_transforms(self.transforms)

    def remove_transforms(self, transforms, by_field=None):
        '''remove transforms by equality or list of field values'''
        if by_field:
            self.transforms = [ t for t in self.transforms if t[by_field] not in transforms ]
        else:
            self.transforms = [ t for t in self.transforms if t not in transforms ]
        self.set_transforms(self.transforms)

    def get_progress(self):
        """Get a json object representing progress of this item"""
        if self.progress:
            client = self._client()
            headers, response = client._request(self.progress)
            unicode_error = False
            try:
                response = response.decode('utf-8', 'strict')
            except UnicodeDecodeError:
                response = response.decode('utf-8', 'replace')
                unicode_error = True
            try:
                progress = json.loads(response)
                if unicode_error:
                    progress['message'] += ' - it looks like an invalid character'
                return progress
            except ValueError,ex:
                _logger.warn('invalid JSON response: %s',response)
                raise RequestFailed('invalid JSON')
        else:
            raise Exception("Item does not have a progress endpoint")


class Session(_UploadBase):
    _object_name = 'import'
    _bindings = (
        _binding("id"),
        #_binding("href"),
        _binding("state"),
        #_binding("archive", expected=False, ro=False),
        _binding("tasks", expected=False, binding=Task),
    )

    def delete_unrecognized_tasks(self):
        """For any tasks that have unrecognized formats, wipe them out."""
        for t in list(self.tasks):
            if t.data.format is None:
                _logger.info("deleting unrecognized task %s", t)
                t.delete()
                self.tasks.remove(t)

    def upload_task(self, files, use_url=False):
        """create a task with the provided files
        files - collection of files to upload or zip file
        use_url - if true, post a URL to the uploader
        """
        # @todo getting the task response updates the session tasks, but
        # neglects to retreive the overall session status field
        fname = os.path.basename(files[0])
        _,ext = os.path.splitext(fname)
        if use_url:
            if ext == '.zip':
                upload_url = files[0]
            else:
                upload_url = os.path.dirname(files[0])
            url = self._url("imports/%s/tasks?expand=3" % self.id)
            upload_url = "file://%s" % os.path.abspath(upload_url)
            resp = self._client().post_upload_url(url, upload_url)
        elif ext == '.zip':
            url = self._url("imports/%s/tasks/%s?expand=3" % (self.id, fname))
            resp = self._client().put_zip(url, files[0])
        else:
            url = self._url("imports/%s/tasks?expand=3" % self.id)
            resp = self._client().post_multipart(url, files)
        tasks = parse_response( resp )
        if not isinstance(tasks, list):
            tasks = [tasks]
        for t in tasks:
            t._parent = self
        self.tasks.extend(tasks)

    def commit(self, async=False):
        """Run the session"""
        #@todo check task status if we don't have it already?
        url = self._url("imports/%s",self.id)
        if async:
            url = url + "?async"
        resp, content = self._client().post(url)
        if resp['status'] != '204':
            raise Exception("expected 204 response code, got %s" % resp['status'],content)

    def delete(self):
        """Delete this import session"""
        url = self._url("imports/%s",self.id)
        resp, content = self._client().delete(url)
        if resp['status'] != '204':
            raise Exception('expected 204 response code, got %s' % resp['status'],content)
    

