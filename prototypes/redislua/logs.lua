if redis.call("LLEN", "logs.test") > 2000 then
    redis.call("LPOP", "logs.test")
end

redis.call("RPUSH", "logs.test",ARGV[1])
return "OK"

