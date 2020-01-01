data = {
    "ok": True,
        "data": [
      {
        "1": "08:30 - 09:50",
        "2": "10:00 - 11:20",
        "3": "11:30 - 12:50",
        "4": "13:30 - 14:50",
        "5": "15:00 - 16:20",
        "6": "16:30 - 17:50"
      },
      {
        "1": [
          {
            "type": 1,
            "subject": "\u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430 1",
            "identificator": "MAT019",
            "building": "B",
            "room": "417"
          }
        ],
        "2": None,
        "3": None,
        "4": None,
        "5": [
          {
            "type": 3,
            "subject": "\u0423\u0437\u0431\u0435\u043a\u0441\u043a\u0438\u0439\/\u0420\u0443\u0441\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a 1",
            "identificator": "RUZ004",
            "building": "C",
            "room": "459"
          }
        ],
        "6": None
      },
      {
        "1": [
          {
            "type": 1,
            "subject": "\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a 1",
            "identificator": "FRL076",
            "building": "C",
            "room": "140"
          }
        ],
        "2": [
          {
            "type": 1,
            "subject": "\u0424\u0438\u0437\u0438\u043a\u0430 1",
            "identificator": "FIZ017",
            "building": "A",
            "room": "435"
          }
        ],
        "3": [
          {
            "type": 1,
            "subject": "\u0424\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043a\u0443\u043b\u044c\u0442\u0443\u0440\u0430 1",
            "identificator": "PHC042",
            "building": "A",
            "room": "\u0421\u043f\u043e\u0440\u0442-\u0437\u0430\u043b 4"
          }
        ],
        "4": [
          {
            "type": 1,
            "subject": "Python 1",
            "identificator": "PRG001",
            "building": "B",
            "room": "03"
          }
        ],
        "5": None,
        "6": None
      },
      {
        "1": [
          {
            "type": 1,
            "subject": "\u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430 1",
            "identificator": "MAT019",
            "building": "B",
            "room": "417"
          }
        ],
        "2": [
          {
            "type": 2,
            "subject": "\u0424\u0438\u0437\u0438\u043a\u0430 1",
            "identificator": "FIZ017-L2",
            "building": "A",
            "room": "428"
          },
          {
            "type": 3,
            "subject": "\u0424\u0438\u0437\u0438\u043a\u0430 1",
            "identificator": "FIZ017-1",
            "building": "A",
            "room": "426"
          }
        ],
        "3": None,
        "4": [
          {
            "type": 1,
            "subject": "Python 1",
            "identificator": "PRG001-L1",
            "building": "B",
            "room": "01"
          }
        ],
        "5": None,
        "6": None
      },
      {
        "1": [
          {
            "type": 1,
            "subject": "\u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430 1",
            "identificator": "MAT019-1",
            "building": "A",
            "room": "420"
          }
        ],
        "2": None,
        "3": None,
        "4": [
          {
            "type": 1,
            "subject": "Python 1",
            "identificator": "PRG001-L1",
            "building": "B",
            "room": "01"
          }
        ],
        "5": None,
        "6": [
          {
            "type": 1,
            "subject": "\u0420\u0435\u043b\u0438\u0433\u0438\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u0435",
            "identificator": "HSM009",
            "building": "C",
            "room": "443"
          }
        ]
      },
      {
        "1": [
          {
            "type": 1,
            "subject": "\u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430 1",
            "identificator": "MAT019-1",
            "building": "A",
            "room": "420"
          }
        ],
        "2": None,
        "3": None,
        "4": [
          {
            "type": 1,
            "subject": "Python 1",
            "identificator": "PRG001-L1",
            "building": "B",
            "room": "01"
          }
        ],
        "5": None,
        "6": [
          {
            "type": 1,
            "subject": "\u0420\u0435\u043b\u0438\u0433\u0438\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u0435",
            "identificator": "HSM009-1",
            "building": "A",
            "room": "32"
          }
        ]
      },
      {
        "1": None,
        "2": [
          {
            "type": 1,
            "subject": "\u041c\u0443\u0440\u0430\u0431\u0431\u0438\u0439\u043b\u0438\u043a \u0441\u043e\u0430\u0442\u0438",
            "identificator": "314-18 \u0414\u0418\u0443",
            "building": "\u0410",
            "room": "315"
          }
        ],
        "3": None,
        "4": None,
        "5": None,
        "6": None
      }
    ]
}

import json

def schedule_reformatter(data):
	result = []
	times = {}
	times_counter = 1
	for i in range(len(data)):
		times[str(i+1)] = data[i]['time']

	result.append(times)
	for day in range(6):
		single = {}
		for pair in range(len(data)):
			if data[pair]['week'][day]['data'] != None:
				single[str(pair+1)] = [data[pair]['week'][day]['data']]
			else:
				single[str(pair+1)] = None
		result.append(single)
	return result

#print(schedule_reformatter(data['data']))