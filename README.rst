########################################
 Entra ID OIDC ID Token Diagnostic Tool
########################################

Displays both the ID Token and UserInfo endpoint result for the
authenticated principal.

Basic usage:

.. code:: shell

   $ ./entra_oidc_id_token.py PATH_TO_CLIENT_INFO_FILE UPN PATH_TO_PASSWORD_FILE

The client info file should contain a JSON object with keys
"metadata_url" and "client_id".
