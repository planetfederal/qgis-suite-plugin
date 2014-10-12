Authentication configurations
##############################

When using a service that requires authentication, such a WMS or WFS connection, QGIS can safely store the connection parameters, making it easier to use them in a future session. Creating and retrieving authentication parameters (an authentication configuration) is done using the auth configuration widget, which looks like this:

.. figure:: widget.png

This widget can be found in connections requiring authentication, usually along with the classic entry for basic authentication (with username and password textboxes).

The dropdown box in the upper-left part of the configurations widget contains a list of all the configurations that have been already define in the current or in previous sessions. IF it is the first time you use it, it will only contain a default entry naed "No authentication"

To add a new configuration, click on the *Add* button. You will see a dialog like the one shown next:

.. figure:: master_password.png

This dialog prompts you to enter a password for the database where all authentication parameters are stored. Data in the database is encripted and it cannot be retrieved form it without using the master password. If you have defined no password before, just enter the password that you want for the auth database, and it will be set as the master password.

Once you have entered the password and you have access to the auth database, QGIS will not ask you again for it during the current session. You can use previous configurations or add new ones, without having to enter the master password again.

The dialog to define a new configuration looks like this

.. figure:: add_new_auth.png

In the *Name* field, enter the name you want to use to refer to this configuration. It will be the name that will be shown in the dropdown box with all existing configurations.

Select the type of authentication that you want to use, from the two available options: username/password or PKI certificates. The elements in the lower part of the dialog will change depending on the selected type, to allow entering the parameters needed for each case. In the case of PKI certificates, the dialog will look like this.

.. figure:: add_new_pki_auth.png

Paths to certificate files have to be entered. Files have to be in PEM format. A single file containing both the private key and certificate is not supported, and two different files hace to be entered. Optionally, a root certificate file can be specified.

Validation of the parameter is implemented, and the validity will be shown once you enter the primary key and certificate files.

.. figure:: certificate_validation.png

Click on OK to add the authentication configuration. It will now appear in the list of available ones. 

.. figure:: auth_confs_list.png

If you want to use that configuration for setting up a connection, now you just have to select it, and there is no need to enter the parameters again. All the configuration settings are safely stored in the auth database.

Managing authentication configuration from the settings window
---------------------------------------------------------------

The settings window (menu *Settings->Options*) contains an entry for authentication configurations. You will see a list of all the existing configurations, and you can edit them, remove them or add new ones.

.. figure:: auth_settings.png

Click on *Reset master password* in case you want to change the master password used to access the auth database.

