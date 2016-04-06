//Go implementation of batarang


package main

import (
    "net"
    "os"
    "os/signal"
    //"io"
    "bufio"
    "encoding/json"
    //"sync"
    "time"
    "fmt"
    "flag"
    "runtime"   
)

//Globals
var localNode Node
var nodeTable NodeTable
//Heart beats tell other nodes that current node is still alive
func heartbeats(port int) {
    BROADCASTIPv4 := net.IPv4(192,168,200,255)
    
    udpAddr:=&net.UDPAddr{
        IP:   BROADCASTIPv4,
        Port: port,
    }
    
    socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
        IP: net.IPv4zero,
        Port: 0,
    })
    check(err)
    defer socket.Close()
    
    var hb = Message{localNode.IP.String(), "HB", "none", time.StampMilli}
    
    for localNode.Alive{
        hb.time = time.Now().Format(time.StampMilli)
        
        data,err := json.Marshal(hb)
        catch(err, hb.String())
        
        n, err := socket.WriteToUDP(data,udpAddr)
        fmt.Printf("%d:\n",n)
        pass(err)
        
        time.Sleep(time.Second * 1)
    }
}

//hbListen listens on port for heartbeats and sends them through the channel
func hbListen(port int, hbChan chan<- Message){
    
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(192,168,200, 0),
        Port: port,
    })
    check(err)
    defer socket.Close()

    data := make([]byte,1024)
    for localNode.Alive {
        
        n,addr,err := socket.ReadFromUDP(data)
        if n > 0{
            fmt.Printf("%d::%v\n",n,addr)
            catch(err,data)
            
            msg := Message{}
            
            err = json.Unmarshal(data,msg)
            check (err)
            
            hbChan<- msg
        }
    }
    
}
//Our loop waiting for input or a keyboard interrupt
func sendLoop(port int, in <-chan Message, q <-chan os.Signal){   
    BROADCASTIPv4 := net.IPv4(192,168,200,255)
    
    udpAddr:=&net.UDPAddr{
        IP:   BROADCASTIPv4,
        Port: port,
    }
    
    socket, err := net.DialUDP("udp4", nil, udpAddr)
    
    check(err)
    defer socket.Close()
    
    for localNode.Alive {
        select{
            case msg:= <-in:
                data := make([]byte,1024)
                
                data,err = json.Marshal(msg)
                catch(err, msg.String())
                
                n, err := socket.WriteTo(data, udpAddr)
                fmt.Printf("%d \n",n)
                pass(err)
                
            case <-q:
                localNode.Alive = false
                nodeTable.ready = false
                return
        }
    }
}
// Listen and pass messages on port to the msg channel
func listen(port int, msgChan chan<- Message){
    
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(192,168,200, 0),
        Port: port,
    })
    check(err)
    defer socket.Close()
    
    data := make([]byte,1024)
    for localNode.Alive{
   
        n,addr,err := socket.ReadFrom(data)
        if n > 0 {
            fmt.Printf("%d::%v \n",n,addr)
            catch(err,data)
            
            msg := Message{}
            
            err = json.Unmarshal(data,msg)
            catch(err,data)
            
            msgChan<- msg
        }
    }
}

// Broadcast messages
func broadcastMsg(msg Message, in chan<- Message){
    for nodeTable.ready == false{
        in <- msg
        time.Sleep(1)
    }
}
//Loop sorting chanels to specific processes
func handleMessages(hbChan,msgChan<-chan Message,outMsg chan Message){

    for localNode.Alive{
        select{
            case hb := <-hbChan:
                fmt.Println(hb)
                nodeTable.handleHB(hb)
                //handle heartbeats
            case msg := <-msgChan:
                fmt.Println(msg)
                nodeTable.handleMsg(msg,outMsg)
                //handle other messages
        }
    }  
}
//Our debug message to send
func fakeMessage(input chan<- Message, q <-chan os.Signal){
    var msg = Message{localNode.IP.String(), "FC", "915000", ""}
    
    for localNode.Alive{
        select{
            case <-q:
                localNode.Alive = false
                nodeTable.ready = false
                return 
            default:
                bufio.NewReader(os.Stdin).ReadBytes('\n')
                msg.time = time.Now().Format(time.StampMilli)
                input <- msg
        }
    }
}


func main() {
    hbPort := 9001
    msgPort := 9000
    arg := flag.Arg(0)
    if arg == ""{
        arg = "bat0"
    }
    
    //Parse Interface
    iface, err := net.InterfaceByName(arg)
    if err != nil{
        ifaces, err := net.Interfaces()
        fmt.Println("Available interfaces are...")  
        for _,i := range ifaces{
            fmt.Println(i.Name)
        }
        check(err)
    }
    
    var ip net.IP
    addrs, err := iface.Addrs()
    check(err)
    for _, addr:= range addrs{
        switch v := addr.(type){
            case *net.IPNet:
                ip = v.IP
            case *net.IPAddr:
                ip = v.IP
        }
    }
    
    //Global Initialization initialization
    localNode = Node{ip,true,true,time.Now()}
    nodeTable = NodeTable{time.Now(),"", make(map[string]*Node), false, 30}
    
    //Channels
    //msg in
    msgChan := make(chan Message)
    defer close(msgChan)
    
    //hb in
    hbChan := make(chan Message)
    defer close(hbChan)
    
    //quit channel
    q:= make(chan os.Signal, 1)
    signal.Notify(q,os.Interrupt)
    defer close(q)
    
    //msg out
    outMsg:= make(chan Message, 1)
    defer close(outMsg)
    
    //runtime
    runtime.GOMAXPROCS(runtime.NumCPU())
    
    //Goroutines
    go handleMessages(hbChan, msgChan,outMsg)
    //Heartbeats
    go heartbeats(hbPort)
    ///Listen for heartbeats
    go hbListen(hbPort,hbChan)
    //listen for messages
    go listen(msgPort, msgChan) 
    //Outgoing messages
    go sendLoop(msgPort,outMsg,q)
    
    fakeMessage(outMsg,q)
}

