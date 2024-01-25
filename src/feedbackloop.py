from kafka import KafkaConsumer
import requests


consumer = KafkaConsumer('movielog2',
                            bootstrap_servers='fall2023-comp585.cs.mcgill.ca:9092',
                            auto_offset_reset='latest',
                            enable_auto_commit=True,)

msgcount = 0
totmsg = 500
fldict = {}
predsdict = {}
usractivedict = {}
usrgenredict = {}

def curl_req(link:str):
    response = requests.get(link)
    return response.json()

for msg in consumer:
    
    msg_value = msg.value.decode('utf-8')

    msgs = msg_value.split(',')
    curuserid = msgs[1]
    response = curl_req('http://fall2023-comp585.cs.mcgill.ca:8080/user/'+str(curuserid))
    if "message" in response:
        continue


    if "GET" in msg_value: 

        if curuserid not in predsdict:
            continue

        try :
            getmsgs = msgs[2].split('/')
            moviewatched = getmsgs[3]

        except Exception as e:
            continue
        
        validmovieresponse = curl_req('http://fall2023-comp585.cs.mcgill.ca:8080/movie/'+moviewatched)


        if "message" in validmovieresponse:
            print("Invalid Movie")
            continue
        

        if curuserid not in usractivedict:
            usractivedict[curuserid] = 1
        else:
            usractivedict[curuserid] += 1

        predsmovies = predsdict[curuserid]

        if moviewatched in predsmovies:
            if curuserid not in fldict:
                fldict[curuserid] = 1
            else:
                fldict[curuserid] += 1
        else : 
            watchedgenres = [d["name"] for d in validmovieresponse["genres"]]
            genres = {}
            for m in predsmovies:
                r = curl_req('http://fall2023-comp585.cs.mcgill.ca:8080/movie/'+m)
                gs = [d["name"] for d in r["genres"]]
                for g in gs:
                    if g not in genres:
                        genres[g] = 1
                    else:
                        genres[g] += 1
            sorte = sorted(genres, key=genres.get, reverse=True)
            sorte = sorte[:5]
            print(sorte)
            c = 0
            for w in watchedgenres:
                print(w)
                if w in sorte:
                    c += 1
            print("This user matches on " + str(c) + " genres")
            if curuserid not in usrgenredict:
                usrgenredict[curuserid] = c
            else:
                if usrgenredict[curuserid] < c:
                    usrgenredict[curuserid] = c
            
        msgcount += 1
        print(msgcount)

    if "recommendation request" in msg_value and "status 200" in msg_value and "result" in msg_value:

        userid = msgs[1]

        index = msg_value.find("result:")

        results_data = msg_value[index + len("result:"):].strip()

        results_list = results_data.split(', ')[:-1]

        predsdict[userid] = results_list

        print("Provided for " + str(len(predsdict)) + " different users.")

    print("Visits : " + str(msgcount))
    if msgcount == totmsg:
        break


print(predsdict)

print(usractivedict)

print(fldict)

print("Total : " + str(sum(usractivedict.values())))
print("Watched our movies : " + str(sum(fldict.values())))

print(usrgenredict)
