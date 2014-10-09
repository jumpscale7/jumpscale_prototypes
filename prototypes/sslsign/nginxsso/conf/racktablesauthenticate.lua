local ba = require"basicauthentication"


local username = 'rob'
local password = 'xxxxxxxxxxxxxx'

ba.set_authentication_header(username, password)
