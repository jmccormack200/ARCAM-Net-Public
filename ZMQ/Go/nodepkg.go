

package main

//Node structure for node data
type Node struct{
    IP      net.IP
    ACK     bool
    Alive   bool
    hbTime  time.Time
}
//Message structure for message data
type Message struct{
    source  string
    msgType string
    msgDat  string
    time    string
}
func (msg Message) String() string{
    return (msg.source + " " + msg.msgType + " " + msg.msgDat + " " + msg.time)
}
//NodeTable structure
type NodeTable struct{
    startTime   time.Time
    header      string 
    nodeDict    map[string]*Node
    ready       bool
    timeout     float32 = 20.0f
}

//flushes table ack
func (table NodeTable)flush(){
    table.startTime = nil
    table.header = ""
    table.ready = false
    for k,_ := range table.nodeDict{
        table.nodeDict[k].ACK = false
    }
}

//Checks to see if table is ready
func (table NodeTable)checkIfReady(){
    ready = true
    for k,v := range table.nodeDict{
        if time.Now() - v.hbTime >= table.timeout{
            v.Alive = false
            table.nodeDict[k] = v
        }      
        if v.ACK == false && v.Alive == true{
            ready = false
            break
        }
    }
    table.ready = ready
    return ready
}


func (table NodeTable)handleMsg(msg Message, inputChan chan Message){
    //case 1: Empty Table
    if table.header == ""{
        table.startTime = time.Now()
        table.header = msg.msgDat
        table.ready = false
        go broadcastMsg(msg,inputChan)
    //case 2: Waiting Table with matching data
    }
    if msg.msgDat == table.header {
          //Case 2.1: node is in table
          if _,ok := table.nodeDict[msg.source]; ok{
              newtime,err := time.Parse(time.StampMilli,msg.time)
              catchstring(err, msg.String())
              table.nodeDict[msg.source].ACK = true
              table.nodeDict[msg.source].Alive = true
              table.nodeDict[msg.source].hbTime = newtime
          //Case 2.2: node is missing in table
          } else {
              newtime,err := time.Parse(time.StampMilli,msg.time)
              catchstring(err,msg.String())
              newNode := Node{
                  IP: net.ParseIP(msg.source),
                  ACK: true,
                  Alive: true,
                  hbTime: newtime,
               }
               table.nodeDict[msg.source] = &newNode
               fmt.Printf("Node %s added to table \n", msg.source)
          }
          fmt.Printf("ACK %v", msg.source)
          
          if table.checkIfReady() {
              //Do something
              table.flush()
          }
    }
}

//Handles heartbeats
func (table NodeTable)handleHB(msg Message){
    //Case 1: node is in table
    if _,ok := table.nodeDict[msg.source]; ok{
        newtime,err := time.Parse(time.StampMilli,msg.time)
        catchstring(err, msg.String())
        table.nodeDict[msg.source].Alive = true
        table.nodeDict[msg.source].hbTime = newtime
        
    //Case 2: node is missing in table
    } else {
        newtime,err := time.Parse(time.StampMilli,msg.time)
        catchstring(err,msg.String())
        newNode := Node{
            IP: net.ParseIP(msg.source),
            ACK: false,
            Alive: true,
            hbTime: newtime,
        }
        table.nodeDict[msg.source] = &newNode
        fmt.Printf("Node (%s) added to table\n", msg.source)
    }
}
