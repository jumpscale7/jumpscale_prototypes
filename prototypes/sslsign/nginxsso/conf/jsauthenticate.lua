local http = require"socket.http"
local ltn12 = require"ltn12"
-- ngx = {}

local sessioncookiekey = 'beaker.session.id'

local reqbody = "user_login_=admin&passwd=xxxxxxxxx"

local respbody = {} -- for the response body

local result, respcode, respheaders, respstatus = http.request {
    method = "POST",
    url = "http://cpu01.bracknell1.vscalers.com:82/",
    source = ltn12.source.string(reqbody),
    headers = {
        ["content-type"] = "application/x-www-form-urlencoded",
        ["content-length"] = tostring(#reqbody)
    },
    sink = ltn12.sink.table(respbody)
}

-- get body as string by concatenating table filled by sink
respbody = table.concat(respbody)

local cookieheader = respheaders['set-cookie']
print("Cookie header:"..cookieheader)

ngx.header['Set-Cookie'] = cookieheader

ngx.req.set_header('Cookie', cookieheader)
