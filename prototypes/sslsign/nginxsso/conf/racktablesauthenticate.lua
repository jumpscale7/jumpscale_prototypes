local mime = require"mime"
local ltn12 = require"ltn12"

local username = 'rob'
local password = 'xxxxxxxxxxxxxxxxxxxxxxxx'

local base64filter = ltn12.filter.chain(
  mime.normalize(),
  mime.encode("base64")
)

local encodedcredentials = {}

sink = ltn12.sink.chain(base64filter, ltn12.sink.table(encodedcredentials))

ltn12.pump.all(ltn12.source.string(username..":"..password), sink)

encodedcredentials = table.concat(encodedcredentials)

ngx.req.set_header('Authorization', 'Basic '..encodedcredentials)
