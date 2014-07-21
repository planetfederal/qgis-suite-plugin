DROP TABLE IF EXISTS ISO_metadata CASCADE;
DROP TABLE IF EXISTS ISO_metadata_reference CASCADE;

CREATE TABLE ISO_metadata
(
	id serial PRIMARY KEY,
	md_scope character varying(64),
	metadata xml,
	fileId xml default null,
	parentId xml default null,
	geometry geometry
)
WITH (
  OIDS=TRUE
);
-- ALTER TABLE ISO_metadata OWNER TO postgres;
-- GRANT ALL ON TABLE ISO_metadata TO postgres;

CREATE TABLE ISO_metadata_reference
(
	reference_scope character varying(64),
	table_name character varying(256),
	column_name character varying(256),
	row_id_value integer,
	timestamp timestamp default statement_timestamp(),
	md_file_id integer references ISO_metadata(id) default 0,
	md_parent_id integer references ISO_metadata(id) default 0
	
)
WITH (
  OIDS=TRUE
);
-- ALTER TABLE ISO_metadata_reference OWNER TO postgres;
-- GRANT ALL ON TABLE ISO_metadata_reference TO postgres;

CREATE OR REPLACE FUNCTION update_imr_timestamp_column()
	RETURNS TRIGGER AS $$
	BEGIN
	   NEW.timestamp = now(); 
	   RETURN NEW;
	END;
	$$ language 'plpgsql';

CREATE TRIGGER update_imr_timestamp BEFORE UPDATE
        ON ISO_metadata_reference FOR EACH ROW EXECUTE PROCEDURE 
        update_imr_timestamp_column();


-- REGISTER ISO METADATA ######################################

CREATE OR REPLACE FUNCTION public.RegisterIsoMetadata(character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
	schema_name alias for $1;
	table_name_alias alias for $2;
	metadata alias for $3;

	sql text;
	ret text;
	tmp text;
	fid xml;
	pid xml;
	geo geometry;
	ns varchar[];

BEGIN    
	ns := ARRAY[ARRAY['gmd', 'http://www.isotc211.org/2005/gmd']];
	IF position('gmd:fileIdentifier' in metadata) <> -1 THEN
		fid := xpath('//gmd:fileIdentifier/*', XMLPARSE(DOCUMENT metadata), ns);
		pid := xpath('//gmd:parentIdentifier/*', XMLPARSE(DOCUMENT metadata), ns);
	ELSE
		fid := xpath('//fileIdentifier/*', XMLPARSE(DOCUMENT metadata), ns);
		pid := xpath('//parentIdentifier/*', XMLPARSE(DOCUMENT metadata), ns);
	END IF;
	geo := BBoxGeometryFromMetadata(metadata);
	tmp := XMLSERIALIZE(CONTENT pid AS text);
	IF tmp = '{}' THEN
		pid := fid;
	END IF;
	sql := 'SELECT GetIsoMetadata(''' || schema_name || ''', ''' || table_name_alias || ''')';
	EXECUTE sql INTO tmp;
	INSERT INTO iso_metadata(md_scope, metadata, fileid, parentid, geometry)
	       VALUES('undefined', XMLPARSE(DOCUMENT metadata), fid, pid, geo); 
	sql := 'SELECT max(id) FROM iso_metadata';
	EXECUTE sql INTO ret;

	IF tmp <> '' THEN
		UPDATE iso_metadata_reference SET md_file_id = cast(ret AS integer), md_parent_id = cast(ret AS integer) 
		       WHERE reference_scope='table' AND table_name = table_name_alias;
	ELSE 
		INSERT INTO iso_metadata_reference(reference_scope, table_name, md_file_id, md_parent_id)
		       VALUES('table', table_name_alias, cast(ret AS integer), cast(ret AS integer));
	END IF;
	RETURN ret;

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public.RegisterIsoMetadata(character varying, character varying, character varying)
  OWNER TO postgres;


-- GET ISO METADATA ######################################

CREATE OR REPLACE FUNCTION public.GetIsoMetadata(character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    schema_name alias for $1;
    table_name alias for $2;

    rowid integer;
    metadata xml;
    sql text;
    ret text;
BEGIN

    sql := 'SELECT md_file_id FROM iso_metadata_reference WHERE column_name IS NULL AND row_id_value IS NULL AND reference_scope=''table'' AND table_name=''' || table_name || ''' LIMIT 1';
    EXECUTE sql INTO rowid;

    IF rowid IS NULL THEN
	RETURN '';
    END IF;

    sql := 'SELECT metadata FROM iso_metadata WHERE id=' || rowid || ' LIMIT 1 ';
    EXECUTE sql INTO metadata;

    RETURN metadata::text;

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public.GetIsoMetadata(character varying, character varying)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION public.BBoxGeometryFromMetadata(character varying)
  RETURNS geometry AS
$BODY$
DECLARE
	src alias for $1;
	tmp text;

	extentPath character varying;

	substract boolean;
	north numeric;
	south numeric;
	east numeric;
	west numeric;

	ns varchar[];

	m xml;
	app xml;
	doc xml[];

	box geometry;
	geo geometry;

BEGIN    
	ns := ARRAY[ARRAY['gmd', 'http://www.isotc211.org/2005/gmd'], 
	            ARRAY['gco', 'http://www.isotc211.org/2005/gco'], 
	            ARRAY['srv', 'http://www.isotc211.org/2005/srv'] ];
	doc := xpath('/gmd:MD_Metadata/gmd:identificationInfo/*/*/gmd:EX_Extent', XMLPARSE(DOCUMENT src), ns);
	FOREACH m IN ARRAY doc
	LOOP
		IF position('gmd:EX_Extent' in XMLSERIALIZE(DOCUMENT m AS text)) <> -1 THEN
			tmp := '<root xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:srv="http://www.isotc211.org/2005/srv">'||regexp_replace(XMLSERIALIZE(DOCUMENT m AS text), 'gmd:', '','g')||'</root>';
		ELSE
			tmp := '<root xmlns="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:srv="http://www.isotc211.org/2005/srv">'||XMLSERIALIZE(DOCUMENT m AS text)||'</root>';
		END IF;
		IF xpath_exists('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox', tmp::xml, ns) THEN
			substract := FALSE;
			IF xpath_exists('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox/extentTypeCode/*', tmp::xml, ns) THEN
				app := xpath('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox/extentTypeCode/*/text()', tmp::xml, ns); --gco:Boolean
				IF app::text = '{0}' OR app::text = '{false}' OR app::text = '{FALSE}' THEN
					substract := TRUE;
				END IF;
			END IF;
			
			app := xpath('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox/westBoundLongitude/*/text()',  tmp::xml, ns);
			west :=substring(app::text FROM '[0-9.-]+')::numeric;
			app := xpath('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox/eastBoundLongitude/*/text()',  tmp::xml, ns);
			east :=substring(app::text FROM '[0-9.-]+')::numeric;
			app := xpath('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox/southBoundLatitude/*/text()',  tmp::xml, ns);
			south :=substring(app::text FROM '[0-9.-]+')::numeric;
			app := xpath('/*/EX_Extent/geographicElement/EX_GeographicBoundingBox/northBoundLatitude/*/text()',  tmp::xml, ns);
			north :=substring(app::text FROM '[0-9.-]+')::numeric;
			
			box := st_astext(ST_MakeBox2D(ST_Point(west, south), ST_Point(east, north)));
			IF geo IS NULL THEN
				geo := box;
			ELSE
				IF substract THEN
					geo := ST_Difference(geo, box);
				ELSE
					geo := ST_Union(geo, box);
				END IF;
			END IF;
		ELSE
			CONTINUE;
		END IF;
		IF geo IS NOT NULL THEN
			geo = ST_ENVELOPE(geo);
		END IF;
	END LOOP;
	RETURN geo;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public.BBoxGeometryFromMetadata(character varying)
  OWNER TO postgres;


