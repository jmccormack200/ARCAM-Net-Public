

package nodepkg



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
}
func (table NodeTable)handleMsg(msg Message){
    //case 1: Empty Table
    if table.header == ""{
        table.startTime = time.Now()
        table.header = msg.msgDat
        table.ready = false
        //go broadcast
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
          //Check Table
    }
}
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
