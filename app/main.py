from flask import Flask,request,jsonify
import sys
import redis

app = Flask(__name__)

#connect redis
r = redis.StrictRedis(host='my-redis-container', port=6379, db=0)

@app.route("/")
def hello():
    return "Hello World from Flask"

@app.route('/autocomplete')
def complete():
#  import pdb; pdb.set_trace()
  prefix=request.args.get('prefix')
  results = []
  grab = 42
  count = 50
  start = r.zrank('autocomplete',prefix)
  if not start:
    return []
  while (len(results) != count):
    range = r.zrange('autocomplete',start,start+grab-1)
    start = start + grab
    if not range or len(range) == 0:
      break
    for entry in range:
      minlen = min(len(entry),len(prefix))
      if entry[0:minlen] != prefix[0:minlen]:
        count = len(results)
        break
      if entry[-1] == "%" and len(results) != count:
        results.append(entry[0:-1])

  return jsonify(results)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
