
import streamlit as st

# ==========================================
# PAGE CONFIG & CLEAN LIGHT CSS
# ==========================================
st.set_page_config(page_title="CNIP Quiz Portal", page_icon="🎓", layout="centered")

st.markdown("""
<style>
    /* Clean White Background */
    .stApp { 
        background-color: #ffffff; 
        color: #1e293b; 
    }
    
    /* Header styling */
    .portal-header { 
        text-align: center; 
        color: #1e3a8a; 
        font-size: 2.2rem; 
        font-weight: 800; 
        margin-bottom: 0px; 
    }
    .portal-sub { text-align: center; color: #64748b; font-size: 0.95rem; margin-bottom: 30px; }
    
    /* Clean Light Cards */
    .week-card { 
        background: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #e2e8f0; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .week-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .week-title { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 5px; }
    
    /* Quiz Top Bar */
    .top-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 20px;}
    .quiz-title { font-size: 1.2rem; font-weight: bold; color: #1e3a8a; }
    .question-count { color: #64748b; font-size: 0.9rem; font-weight: bold;}
    
    /* Results Review Box */
    .review-box { 
        background: #f8fafc; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        border: 1px solid #e2e8f0; 
    }
    
    /* Instant Feedback Boxes */
    .ans-correct { background-color: #d1fae5; border: 1px solid #10b981; padding: 12px; border-radius: 8px; color: #065f46; margin-top: 15px; font-weight: 600;}
    .ans-wrong { background-color: #fee2e2; border: 1px solid #ef4444; padding: 12px; border-radius: 8px; color: #991b1b; margin-top: 15px; font-weight: 600;}
    .explanation { background-color: #f1f5f9; padding: 12px; border-radius: 8px; color: #334155; font-size: 0.95rem; margin-top: 5px; line-height: 1.5; border-left: 4px solid #64748b;}
    
    /* Fix Radio Button Text Color for Light Theme */
    .stRadio label { color: #0f172a !important; font-weight: 500; }
    
    /* BUTTON STYLING */
    div[data-testid="stButton"] > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #ef4444;
        color: white;
        border: none;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #dc2626;
        color: white;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3);
    }

    div[data-testid="stButton"] > button:not([kind="primary"]) {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #94a3b8;
    }
    div[data-testid="stButton"] > button:not([kind="primary"]):hover {
        background-color: #f1f5f9;
        border-color: #64748b;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_week' not in st.session_state:
    st.session_state.current_week = None
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

def change_page(page_name):
    st.session_state.page = page_name

def start_quiz(week):
    st.session_state.current_week = week
    st.session_state.q_index = 0
    st.session_state.user_answers = {}
    if week == "Final Exam":
        st.session_state.page = 'final_exam'
    else:
        st.session_state.page = 'quiz'

def next_question():
    st.session_state.q_index += 1

def prev_question():
    st.session_state.q_index -= 1

# ==========================================
# FULL 12 WEEKS DATA
# ==========================================
quiz_data = {
    "Week 1": [
        {"question": "1. Map the devices with their associated layer in the TCP/IP model.\nA. NIC 1. Physical Layer\nB. Router 2. Data Link Layer\nC. Bridge 3. Network Layer\nD. Hub 4. Transport Layer", "options": ["a) A-2, B-3, C-2, and D-1", "b) A-3, B-3, C-2, and D-1", "c) A-3, B-3, C-1, and D-2", "d) A-2, B-3, C-2, and D-2"], "answer": "a) A-2, B-3, C-2, and D-1", "solution": "Hub operates at Layer 1 of the TCP/IP model, while Bridge, NIC, and Switch(L2) work with MAC addresses at Layer 2. A Router works with IP addresses and it operates in a network layer."},
        {"question": "2. Which of the following is/are true with respect to Bridge?\n(i) Also called 'smarter hub'\n(ii) It filters network traffic based on MAC address", "options": ["a) Only (i)", "b) Only (ii)", "c) Both (i) and (ii)", "d) Either (i) or (ii)"], "answer": "c) Both (i) and (ii)", "solution": "A bridge is often called a smarter hub because it forwards and filters network traffic intelligently using MAC addresses, making both statements true."},
        {"question": "3. Which of the following statement(s) are concerned with encapsulation in computer networks?\nI. It involves an addition of a header and trailer to the actual data as it moves down in the TCP/IP protocol stack.\nII. At the transport layer, encapsulation includes port numbers and at the network layer, encapsulation includes IP addresses.", "options": ["a) Only (I)", "b) Only (II)", "c) Both (I) and (II)", "d) Neither (I) nor (II)"], "answer": "c) Both (I) and (II)", "solution": "Encapsulation is the process of addition of a header and trailer while moving down from upper layer to lower layer like adding source and destination port numbers to the application layer data, adding source and destination IP addresses to the transport layer segment etc."},
        {"question": "4. Which of the following is NOT a disadvantage of the circuit switching technique over the packet switching technique in computer networks?", "options": ["a) Delay in the establishment of a dedicated connection between two hosts", "b) Inefficient utilization of the resources", "c) Less scalable", "d) Provides a dedicated communication path between two end hosts"], "answer": "d) Provides a dedicated communication path between two end hosts", "solution": "Circuit switching techniques establish a dedicated path for communication (which is an advantage), although it remains unutilised in case of no data transmission. It also suffers from greater setup time delay, scalability issues, lack of fault tolerance, etc."},
        {"question": "5. What is socket address?", "options": ["a) Combination of port and IP address", "b) Combination of MAC and IP address", "c) IP address only", "d) None of this"], "answer": "a) Combination of port and IP address", "solution": "socket address is the combination of port and IP address. Number socket is an internal terminal for transferring and receiving data/packets at a single node in a computer network."},
        {"question": "6. Which layer collects a stream of bits into a frame?", "options": ["a) Physical Layer", "b) Network Layer", "c) Data Link Layer", "d) Session Layer"], "answer": "c) Data Link Layer", "solution": "The Data Link Layer (Layer 2) of the OSI model is responsible for collecting a stream of bits from the physical layer and assembling them into a meaningful unit called a frame."},
        {"question": "7. Which transport layer protocol will be chosen by an application that does not require any reliability?", "options": ["a) TCP", "b) UDP"], "answer": "b) UDP", "solution": "User Datagram Protocol (UDP) is a connectionless-oriented protocol and provides no reliability."},
        {"question": "8. What is the First search-engine?", "options": ["a) Chrome", "b) Internet Explorer", "c) HotBot", "d) Archie"], "answer": "d) Archie", "solution": "Archie is widely considered the first search engine."},
        {"question": "9. Choose the statement(s) that correctly describe(s) the roles and responsibilities of the Network Interface Card (NIC) in the computer networks.\nI. NIC takes over the responsibility of segmenting large chunks of data into smaller packets that can be transmitted over the networks.\nII. It converts digital data from the computer's processor to an analog signal.", "options": ["a) Only (I)", "b) Only (II)", "c) Both (I) and (II)", "d) Neither (I) nor (II)"], "answer": "c) Both (I) and (II)", "solution": "The NIC's primary role at the Data Link Layer is to ensure reliable frame-based transmission of data over a local network, including responsibilities for framing, MAC addressing, error detection, flow control, and managing access to the transmission medium."},
        {"question": "10. What is the size of IP address (IPv4) in bytes?", "options": ["a) 4", "b) 32", "c) 16", "d) 10"], "answer": "a) 4", "solution": "IP (IPV4) address is 32 bits long that is 4 bytes."}
    ],
    "Week 2": [
        {"question": "1. Is host.xyz.com. a fully qualified domain name?", "options": ["a) True", "b) False"], "answer": "a) True", "solution": "The given domain name ends in a 'dot'. So it is fully qualified."},
        {"question": "2. What makes FTP more secure than TFTP (Trivial File Transfer Protocol)?", "options": ["a) TFTP lacks features like user authentication and secure data transfer mechanisms.", "b) TFTP allows simultaneous connections without encryption.", "c) TFTP uses TCP, which is inherently less secure than UDP.", "d) TFTP is designed for unreliable networks, making it inherently less secure."], "answer": "a) TFTP lacks features like user authentication and secure data transfer mechanisms.", "solution": "Compared to FTP, which uses TCP and has authentication mechanisms, TFTP is less dependable and safe since it lacks crucial security features like user authentication and runs on UDP."},
        {"question": "3. In the HTTP architecture, which of the following best describes a Uniform Resource Locator (URL)?", "options": ["a) A secure protocol for encrypting HTTP communication.", "b) A client-side scripting language for web development.", "c) A unique identifier for resources, including the protocol, hostname, and path", "d) A header that allows caching of web pages for better performance."], "answer": "c) A unique identifier for resources, including the protocol, hostname, and path", "solution": "A URL uniquely identifies resources on the web, specifying the protocol (e.g., HTTP or HTTPS), hostname (e.g., example.com), port (if applicable), and the path to the resource."},
        {"question": "4. Which of the following is the correct syntax for anchor tags in HTML?", "options": ["a) <p>...</p>", "b) <ar>...</ar>", "c) <a>...</a>", "d) <b>...</b>"], "answer": "c) <a>...</a>", "solution": "Example:- <a href=http://host.xyz.com> Link </a>"},
        {"question": "5. Which of the following is correct for statements P, Q and R?\nP: HTTP uses TCP port 80 for communication.\nQ: TELNET transmits data in an encrypted format.\nR: DNS can operate on both TCP and UDP.", "options": ["a) Both P and R is False, Only Q is True", "b) Both P and R is True, Q is False", "c) Only Q is True", "d) Only R is False"], "answer": "b) Both P and R is True, Q is False", "solution": "P: True. Q: False. TELNET transmits data in plaintext, making it unencrypted and insecure. R: True. DNS typically runs on UDP for queries but switches to TCP for zone transfers or large responses."},
        {"question": "6. What is the correct syntax to be written in the command line to initiate a Telnet connection to the web server of www.iitkgp.ac.in?", "options": ["a) telnet//www.iitkgp.ac.in", "b) telnet:www.iitkgp.ac.in", "c) telnet://www.iitkgp.ac.in", "d) telnet www.iitkgp.ac.in"], "answer": "d) telnet www.iitkgp.ac.in", "solution": "The command starts with Telnet, followed by the hostname or IP address."},
        {"question": "7. Which of the following protocols allow non-ASCII data to be sent over email?", "options": ["a) IMAP4", "b) TELNET", "c) MIME", "d) POP3"], "answer": "c) MIME", "solution": "MIME transforms data into a format that SMTP can transmit, such as Base64 encoding for binary files, allowing non-ASCII data to be sent over email."},
        {"question": "8. Which of the following is true about the mail transfer protocol?\nS1: Can send image files with the help of IMAP4\nS2: Can send image files with the help of POP3\nS3: IMAP4 is more secure than POP3", "options": ["a) Only S1", "b) Only S2", "c) S2 and S3 only", "d) S3 Only"], "answer": "d) S3 Only", "solution": "S1: Incorrect. SMTP cannot send image files directly. S2: Incorrect. POP3 is used for retrieving emails. S3: Correct. IMAP4 is generally more secure than POP3."},
        {"question": "9. Which of the following is/are not an Application Layer protocol(s) ?", "options": ["a) HTTP", "b) SFTP", "c) UDP", "d) SNMP"], "answer": "c) UDP", "solution": "UDP is a Transport Layer protocol."},
        {"question": "10. What is the command used by DNS to translate a fully qualified domain name into its corresponding IP address?", "options": ["a) iplookup", "b) nssearch", "c) ipconfig", "d) nslookup"], "answer": "d) nslookup", "solution": "nslookup translate fully qualified domain names to corresponding IP addresses."}
    ],
    "Week 3": [
        {"question": "1. Flow control is mainly implemented in", "options": ["a) Physical Layer", "b) Application Layer", "c) Transport Layer", "d) Session Layer"], "answer": "c) Transport Layer", "solution": "Flow control is mainly a function of the Transport Layer."},
        {"question": "2. What kind of sequence number does TCP use?", "options": ["a) byte-oriented sequence number", "b) packet-oriented sequence number", "c) Randomly generated fixed sequence numbers", "d) none of them"], "answer": "a) byte-oriented sequence number", "solution": "TCP uses byte-oriented sequence numbering to ensure reliable, ordered, and efficient data transmission over a network."},
        {"question": "3. Which of the following services is NOT supported by the transport layer?", "options": ["a) End-to-end packet delivery", "b) Ordered packet delivery", "c) Reliable data delivery", "d) Forwarding the datagram from one hop to another hop in the network"], "answer": "d) Forwarding the datagram from one hop to another hop in the network", "solution": "The transport layer provides services like End-to-end packet delivery... The hop-to-hop network packet forwarding is supported by data link layer and network layer."},
        {"question": "4. Transport layer is implemented in the Firmware of a computer system.", "options": ["a) True", "b) False"], "answer": "b) False", "solution": "Transport layer is implemented in the kernel."},
        {"question": "5. A data of 40 bytes need to be delivered using TCP protocol but a sender can send a segment of maximum size 12 bytes only. Identify the sequence number of the last segment formed if the sequence number field uses 5 bits only? [Assume sequence number starts from 0]", "options": ["a) 1", "b) 4", "c) 12", "d) 31"], "answer": "b) 4", "solution": "5 bits = 0 to 31. Seg 1 (0-11), Seg 2 (12-23), Seg 3 (24-31 & 0-3), Seg 4 (4-7). Last segment sequence number is 4."},
        {"question": "6. Timestamping a network packet is necessary for\n(i) Enabling time synchronization across router in network layer\n(ii) For defining packet lifetime.", "options": ["a) Only (i)", "b) Only (ii)", "c) Both (i) and (ii)", "d) None of above"], "answer": "c) Both (i) and (ii)", "solution": "Timestamping is required for both defining packet lifetime and ensuring time synchronization across router in network layer."},
        {"question": "7. Determine whether the following information is True or False?\n'During the three-way handshaking... Delayed duplicate SYN can be handled by TCP at Host 2 simply by ignoring it, as the sequence number is invalid'", "options": ["a) True", "b) False"], "answer": "a) True", "solution": "A delayed duplicate SYN will have an outdated sequence number that doesn't match the current connection state at Host 2 and can be ignored as invalid sequence number."},
        {"question": "8. TCP instance uses a sliding window protocol in the noisy channel. A timeout occurs... Mark the RIGHT statement among the following-", "options": ["a) In Go-Back-N ARQ, if any segment lost, all segments retransmitted. Selective Repeat ARQ, only lost packets.", "b) In Go-Back-N ARQ, only lost packets retransmitted. Selective Repeat ARQ, all packets.", "c) Both cases all packets.", "d) Both cases only lost packets."], "answer": "a) In Go-Back-N ARQ, if any segment lost, all segments retransmitted. Selective Repeat ARQ, only lost packets.", "solution": "In Go-Back-N ARQ, if any segment of the sliding window is lost, all the segments of the corresponding sliding window are retransmitted while in Selective Repeat ARQ, only the lost packets are selectively transmitted."},
        {"question": "9. What is known as outstanding frames?", "options": ["a) Frames that are yet to be transmitted", "b) Frames that have been transmitted, but not yet acknowledged", "c) Acknowledged frames", "d) None of the above"], "answer": "b) Frames that have been transmitted, but not yet acknowledged", "solution": "Frames that have been transmitted, but not yet acknowledged are known as outstanding frames."},
        {"question": "10. TCP three-way handshake. Client ISN: 100, Server ISN: 300. RTT: 80ms. ACK from client delayed, takes 100ms. How much time to establish connection?", "options": ["a) 100ms", "b) 280ms", "c) 180ms", "d) 260ms"], "answer": "c) 180ms", "solution": "Time = (SYN time + SYN+ACK time + ACK time) = 80/2 + 80/2 + 100 = 180ms."}
    ],
    "Week 4": [
        {"question": "1. Let the maximum TCP payload be given 1450 Bytes; then what is the maximum network layer payload in Bytes?", "options": ["a) 1450 Bytes", "b) 1470 Bytes", "c) 1430 Bytes", "d) 1480 Bytes"], "answer": "b) 1470 Bytes", "solution": "The TCP header size is 20 Bytes. So, the maximum network layer payload is (Max TCP payload + TCP header size)=1450+20=1470 Bytes."},
        {"question": "2. In a distributed system, a server advertises a receiver window of 0... application frees up space, but updated ack lost. What should the client do to prevent deadlock?", "options": ["a) Wait indefinitely", "b) Resend data packets", "c) Use a keep-alive mechanism", "d) Close the connection"], "answer": "c) Use a keep-alive mechanism", "solution": "A keep-alive mechanism allows the client to periodically probe the server for updated buffer availability without retransmitting data, preventing deadlock."},
        {"question": "3. Which of the following statement(s) is/are true for the Transport Layer?\n(i) The transport layer protocol should be Stateful.\n(ii) Uses FTP protocols for ensuring flow control.", "options": ["a) Only (i)", "b) Only (ii)", "c) Both (i) and (ii)", "d) None of the above"], "answer": "a) Only (i)", "solution": "We need a stateful protocol for the transport layer. Moreover, ARQ protocols are used to ensure flow control (not FTP)."},
        {"question": "4. A TCP connection is experiencing high delays and packet reordering. Which features of TCP help maintain reliable and ordered communication in this scenario?\n(i) Sequence numbers\n(ii) Acknowledgment numbers\n(iii) Urgent pointer\n(iv) Sliding window", "options": ["a) (i), (iii), (iv)", "b) (i), (ii), (iii)", "c) (ii), (iii), (iv)", "d) (i), (ii), (iv)"], "answer": "d) (i), (ii), (iv)", "solution": "Sequence and acknowledgment numbers allow TCP to reorder. Sliding window ensures efficient transfer. Urgent pointer is unrelated."},
        {"question": "5. In the TCP connection release process, why does the active closer enter the TIME-WAIT state after receiving the final acknowledgment?", "options": ["a) To confirm other host received FIN", "b) To allow resend data", "c) To ensure that any delayed packets in the network are discarded", "d) To avoid reusing the same port"], "answer": "c) To ensure that any delayed packets in the network are discarded", "solution": "The TIME-WAIT state ensures that all delayed packets in the network from the just-closed connection are discarded."},
        {"question": "6. Consider a network with a link bandwidth of 1 Mbps, a delay of 1ms, and a segment size of 1 KB. Which of the following relationships is between BDP and segment size?", "options": ["a) BDP = 8 x (segment size)", "b) BDP/4 = segment size", "c) BDP/8 = segment size", "d) BDP x 8 = segment size"], "answer": "d) BDP x 8 = segment size", "solution": "BDP = 1 Mbps x 1 ms = 1 Kb; segment size = 1 KB = 8 x 1 Kb = 8 x BDP."},
        {"question": "7. The use of a cryptographic function to generate sequence numbers for TCP connection is helpful to avoid", "options": ["a) TCP Congestion Overflow", "b) DoS attack", "c) TCP SYN flood attack", "d) None of these"], "answer": "c) TCP SYN flood attack", "solution": "TCP SYN flood attacks can be prevented by generating sequence numbers using cryptographic functions."},
        {"question": "8. A transport-layer protocol using AIMD starts with an initial sending rate of 1 Mbps. After four successful additive increases (each adding 0.5 Mbps), it detects packet loss. If multiplicative decrease is 0.5, what is the new rate?", "options": ["a) 2.5 Mbps", "b) 1 Mbps", "c) 3 Mbps", "d) 1.5 Mbps"], "answer": "d) 1.5 Mbps", "solution": "Initial: 1 Mbps. Four increases: 1 + 4*0.5 = 3 Mbps. Multiplicative decrease: 3 * 0.5 = 1.5 Mbps."},
        {"question": "9. Which of the following conditions does not influence the segment size in TCP?", "options": ["a) MTU of underlying link", "b) Receiver's advertised window size", "c) Network congestion window size", "d) Header length of the IP protocol"], "answer": "d) Header length of the IP protocol", "solution": "The Header Length of the IP Protocol does not directly affect the TCP segment size."},
        {"question": "10. In the case of a simultaneous TCP open, which of the following are true?\n(i) Both transition to SYN-RECEIVED\n(ii) Handshake completes with SYN+ACK\n(iii) Both move to ESTABLISHED after SYN\n(iv) Less secure", "options": ["a) (i) and (ii)", "b) (iii) and (iv)", "c) All are True", "d) All are False"], "answer": "a) (i) and (ii)", "solution": "In a simultaneous open, both hosts send SYN packets and transition to SYN-RECEIVED. Handshake proceeds normally. Security is not compromised."},
    ],
    "Week 5": [
        {"question": "1. Sender Window in TCP can be given as:", "options": ["a) max(Congestion Window, Receiver Window)", "b) Congestion Window", "c) Receiver Window", "d) min(Congestion Window, Receiver Window)"], "answer": "d) min(Congestion Window, Receiver Window)", "solution": "The Sender Window is computed as the minimum of the Congestion Window and the Receiver Window."},
        {"question": "2. What is the advantage of an iterative server over a concurrent server?", "options": ["a) It handles multiple requests faster.", "b) It is easier to implement and debug.", "c) It supports asynchronous I/O.", "d) It has lower response times for high-traffic scenarios."], "answer": "b) It is easier to implement and debug.", "solution": "An iterative server is simpler to implement and debug due to its sequential nature."},
        {"question": "3. Which of the following uses UDP?", "options": ["a) DNS", "b) POP", "c) HTTP", "d) FTP"], "answer": "a) DNS", "solution": "DNS primarily uses UDP on port 53 for speed and efficiency."},
        {"question": "4. What impact does a higher alpha value have on Jacobson's algorithm?", "options": ["a) It makes SRTT more sensitive to sudden RTT changes.", "b) It reduces the impact of new RTT measurements on SRTT.", "c) It increases the weight of RTTVAR in the RTO calculation.", "d) It eliminates the need for RTTVAR."], "answer": "b) It reduces the impact of new RTT measurements on SRTT.", "solution": "A higher alpha places more emphasis on historical RTT values, reducing the influence of new RTT measurements."},
        {"question": "5. FD_ZERO is used for", "options": ["a) tests to see if a file descriptor is part of the set", "b) Initializes the file descriptor set FD_SET - a bitmap of fixed size", "c) Set a file descriptor as a part of an fd_set", "d) None of the above"], "answer": "b) Initializes the file descriptor set FD_SET - a bitmap of fixed size", "solution": "FD_ZERO initializes an fd_set by clearing all bits, so the set starts empty."},
        {"question": "6. SOCK_DGRAM represents", "options": ["a) UDP-based Datagram Socket", "b) TCP-based Stream Socket", "c) QUIC-based Stream Socket", "d) None of the above"], "answer": "a) UDP-based Datagram Socket", "solution": "SOCK_DGRAM represents a UDP-based Datagram Socket."},
        {"question": "7. select() system call returns one when?", "options": ["a) Exactly one monitored file descriptor becomes ready for read/write or reports an error condition.", "b) This means the call timed out", "c) Zero is the number of sockets that have events pending", "d) OS kills the process."], "answer": "a) Exactly one monitored file descriptor becomes ready for read/write or reports an error condition.", "solution": "select() returns 1 when exactly one file descriptor is ready for I/O or has an exceptional (error) condition."},
        {"question": "8. What does the listen() function do in socket programming?", "options": ["a) It binds a socket to an address.", "b) It puts the socket into a passive mode to wait for incoming connections.", "c) It actively connects to a server socket.", "d) It sends data over the socket."], "answer": "b) It puts the socket into a passive mode to wait for incoming connections.", "solution": "The listen() function sets up a socket to accept incoming connections by placing it in passive listening mode."},
        {"question": "9. Which of the following is false?", "options": ["a) TCP uses congestion control", "b) TCP uses both flow control and congestion control", "c) TCP uses flow control", "d) TCP doesn't have any flow control, congestion control"], "answer": "d) TCP doesn't have any flow control, congestion control", "solution": "TCP has flow control, congestion control. So option (d) is false."},
        {"question": "10. Which function can be used to configure socket options like timeout or buffer size?", "options": ["a) setsockopt()", "b) sockopt()", "c) configure()", "d) options()"], "answer": "a) setsockopt()", "solution": "The setsockopt() function is used to configure various socket options."}
    ],
    "Week 6": [
        {"question": "1. In communication over an ISP, which of the following is responsible for determining the best path for packet delivery?", "options": ["a) Transport Layer", "b) Network Layer", "c) Data Link Layer", "d) Application Layer"], "answer": "b) Network Layer", "solution": "The network layer, using routing protocols and IP, determines the best path for packet delivery."},
        {"question": "2. You need 500 subnets, each with about 100 usable host addresses per subnet. What network mask will you assign using a class B network address?", "options": ["a) 255.255.255.252", "b) 255.255.255.128", "c) 255.255.255.0", "d) 255.255.254.0"], "answer": "b) 255.255.255.128", "solution": "Class B default netmask is 255.255.0.0. To have 500 subnets, 9 more bits are required. So netmask will be 255.255.255.128."},
        {"question": "3. What type of address is '0.0.0.0' in IPv4?", "options": ["a) Loopback address", "b) Default route address", "c) Broadcast address", "d) Unspecified address"], "answer": "d) Unspecified address", "solution": "'0.0.0.0' is used to indicate an unspecified address, often during the bootstrapping process."},
        {"question": "4. What is the primary function of the network layer in the TCP/IP model?", "options": ["a) Establish end-to-end connections", "b) Ensure reliable data transfer", "c) Handle logical addressing and routing of data.", "d) Encrypt and decrypt data"], "answer": "c) Handle logical addressing and routing of data.", "solution": "The network layer is responsible for logical addressing (e.g., IP addresses) and routing data packets across networks."},
        {"question": "5. When communicating between two nodes, what role does the transport layer protocol play?", "options": ["a) Routing the data packets.", "b) Providing logical addressing", "c) Ensuring reliable or fast data delivery based on protocol choice.", "d) Forwarding the data to the next hop"], "answer": "c) Ensuring reliable or fast data delivery based on protocol choice.", "solution": "Transport layer protocols like TCP ensure reliable delivery, while UDP provides faster but less reliable delivery."},
        {"question": "6. Which of the following is/are not a valid IPv6 address?", "options": ["a) AE82::1:800:23E7:F5DB", "b) FC80:2:7:1:800:23E7:A:F5DB", "c) DE62:6A42:1:5AC::800:23E7:F5DB", "d) FE80:2030:31:24"], "answer": "d) FE80:2030:31:24", "solution": "Option (d) is invalid because an IPv6 address must have 8 groups, but FE80:2030:31:24 has only 4 groups, making it incomplete."},
        {"question": "7. What is the maximum number of hosts under class B addresses?", "options": ["a) 254", "b) 65534", "c) 65535", "d) 65536"], "answer": "b) 65534", "solution": "With 16 bits total for host, 2^16 = 65,536. Minus two reserved addresses (lowest and highest), yielding 65,534 hosts."},
        {"question": "8. The header length of the IPv6 datagram is", "options": ["a) 10 bytes", "b) 20 bytes", "c) 30 bytes", "d) 40 bytes"], "answer": "d) 40 bytes", "solution": "IPv6 has 40 bytes header length."},
        {"question": "9. What is the CIDR notation for a supernet that aggregates 192.168.0.0/24 and 192.168.1.0/24?", "options": ["a) /23", "b) /24", "c) /25", "d) /22"], "answer": "a) /23", "solution": "The supernet 192.168.0.0/23 includes both 192.168.0.0/24 and 192.168.1.0/24."},
        {"question": "10. How does a Layer 3 switch differ from a Layer 2 switch?", "options": ["a) It uses MAC addresses for packet forwarding.", "b) It performs routing based on IP addresses.", "c) It cannot be used in VLAN environments.", "d) It only operates in the physical layer."], "answer": "b) It performs routing based on IP addresses.", "solution": "A Layer 3 switch performs routing using IP addresses, unlike a Layer 2 switch that relies on MAC addresses for forwarding."}
    ],
    "Week 7": [
        {"question": "1. What is the transmission delay for pushing a packet of size 1MB through a network with a bandwidth 16Mbps?", "options": ["a) 2 seconds", "b) 0.5 seconds", "c) 1 second", "d) 10 second"], "answer": "b) 0.5 seconds", "solution": "Since network bandwidth is 16Mbps so for sending 8Mb (1MB) of data through the network it will take 0.5 seconds."},
        {"question": "2. File transfer applications require non-real-time variable bit rate (NRT-VBR).", "options": ["a) True", "b) False"], "answer": "b) False", "solution": "File transfer is an available bit-rate (best-effort) application."},
        {"question": "3. The primary goal of QoS is", "options": ["a) Degrade loss characteristics.", "b) Control jitter", "c) Increase communication latency", "d) Reduce network security mechanisms"], "answer": "b) Control jitter", "solution": "The primary goal of QoS is to control jitter, improve loss characteristics and decrease communication latency."},
        {"question": "4. Which of the following statements is TRUE?", "options": ["a) TCP is Inelastic... not preferred for real-time video", "b) TCP is Elastic... preferred for real-time video", "c) UDP is Elastic... preferred for real-time video", "d) UDP is Inelastic Traffic and therefore preferred for real-time video streaming."], "answer": "d) UDP is Inelastic Traffic and therefore preferred for real-time video streaming.", "solution": "UDP is typically preferred for real-time video because it avoids overhead."},
        {"question": "5. Based on QoS requirements, video conferencing comes under which class of application?", "options": ["a) Constant bit rate", "b) Real-time variable bit rate", "c) Non-real-time variable bitrate", "d) Available bit rate or best-effort"], "answer": "b) Real-time variable bit rate", "solution": "Video conferencing operates as Real-time variable bit rate."},
        {"question": "6. Which of the following is not a benefit of traffic shaping?", "options": ["a) Reducing network congestion", "b) Controlling the rate of traffic flow", "c) Improving network efficiency", "d) Prioritizing certain types of traffic"], "answer": "d) Prioritizing certain types of traffic", "solution": "Buffering packets to smooth out bursts of traffic is traffic shaping... prioritization is generally scheduling."},
        {"question": "7. Which of the following is an example of a traffic scheduling algorithm?", "options": ["a) Weighted Fair Queuing (WFQ)", "b) Leaky Bucket", "c) Token Bucket", "d) Random Early Detection (RED)"], "answer": "a) Weighted Fair Queuing (WFQ)", "solution": "Weighted Fair Queuing (WFQ) is an example of a traffic scheduling algorithm."},
        {"question": "8. Consider the token bucket algorithm, with token arrival rate = packet arrival rate = r per second. Bucket size is b. What is the maximum burst size (MBS) and the output rate?", "options": ["a) rb and r+b", "b) No burst and rb", "c) No burst and r", "d) r+b and rb"], "answer": "c) No burst and r", "solution": "Since the rate of token arrival is the same as the rate of packet arrival, the bucket will always have enough tokens. Therefore there will not be any burst."},
        {"question": "9. Which of the following statements about Resource Reservation Protocol (RSVP) is FALSE?", "options": ["a) RSVP is difficult to implement on the internet...", "b) All the RSVP daemons... need to coordinate", "c) RSVP uses differentiated services fields in the IP header for traffic classification.", "d) RSVP is a protocol of the Integrated Service (IntServ) QoS architecture."], "answer": "c) RSVP uses differentiated services fields in the IP header for traffic classification.", "solution": "RSVP is typically IntServ, not DiffServ."},
        {"question": "10. In a network with a maximum queue size of 100 packets... threshold 40 to 90 using RED. Current size 70. Drop probability?", "options": ["a) 20%", "b) 40%", "c) 60%", "d) 80%"], "answer": "a) 20%", "solution": "The midpoint of the range (40 to 90) is 65. At size 70 (distance 5 from midpoint), drop probability is typically around 20%."}
    ],
    "Week 8": [
        {"question": "1. How does the router decide the destination if multiple entries in routing tables match?", "options": ["a) It picks the first one", "b) It picks the destination with the longest prefix matching", "c) It picks the destination with the shortest prefix matching", "d) It picks the last matched"], "answer": "b) It picks the destination with the longest prefix matching", "solution": "Routers use longest prefix match to decide routing."},
        {"question": "2. Which routing protocol is used for intra-domain routing in the Internet?", "options": ["a) BGP", "b) RIP", "c) Open Shortest Path First (OSPF)", "d) EIGRP"], "answer": "c) Open Shortest Path First (OSPF)", "solution": "OSPF is an intra-domain link-state routing protocol."},
        {"question": "3. In the BGP protocol, UPDATE and NOTIFICATION messages are used for:", "options": ["a) Exchanging reachability information and to notify an error.", "b) Exchanging reachability and Confirming connection", "c) Ensuring neighbor alive and Confirming connection", "d) Opening and Closing connection"], "answer": "a) Exchanging reachability information and to notify an error.", "solution": "UPDATE messages exchange routes, NOTIFICATION messages signal errors."},
        {"question": "4. Why do we consider dividing an IP address into network address and host address?", "options": ["a) To increase total number", "b) Routers route based on host address", "c) To avoid the overhead of storing all possible host IP addresses in each router.", "d) For resolving IP addresses from domain name"], "answer": "c) To avoid the overhead of storing all possible host IP addresses in each router.", "solution": "By using the network address, routers forward packets without storing every host address."},
        {"question": "5. Router A table: 192.168.1.0/24 -> B, 192.168.1.128/28 -> D, 192.168.2.0/24 -> C. Packet for 192.168.1.10 goes to?", "options": ["a) D", "b) B", "c) C", "d) Broadcast"], "answer": "b) B", "solution": "192.168.1.10 is in the 192.168.1.0/24 subnet, so next hop is B."},
        {"question": "6. When you connect your PC to the internet, how does it know its IP and Gateway without manual configuration?", "options": ["a) DNS", "b) Routing table", "c) ARP", "d) Dynamic Host Configuration Protocol (DHCP)"], "answer": "d) Dynamic Host Configuration Protocol (DHCP)", "solution": "DHCP automatically assigns IP addresses and gateway configuration."},
        {"question": "7. Which data structures are used for speeding up Longest Prefix Matching?", "options": ["a) Double Linked List", "b) Segment Trees", "c) Red Black Trees", "d) Patricia Trees"], "answer": "d) Patricia Trees", "solution": "Patricia Trees store routes bit by bit for efficient longest prefix search."},
        {"question": "8. Which is TRUE about BGP routing protocol?", "options": ["a) Intradomain protocol", "b) Link State protocol", "c) BGP relies on IGP for packet forwarding between IBGP peers.", "d) Replaces IGP"], "answer": "c) BGP relies on IGP for packet forwarding between IBGP peers.", "solution": "BGP relies on IGP like OSPF to route traffic between internal BGP peers."},
        {"question": "9. Assuming Patricia Tree for IPv4 routing table, what is the time complexity of forwarding?", "options": ["a) O(n^2)", "b) O(32)", "c) O(n)", "d) O(logn)"], "answer": "b) O(32)", "solution": "Maximum height of tree is 32 bits, so time complexity is O(32)."},
        {"question": "10. Distance vector: A->Z is 8. C->Z is 6. D->Z is 8. A receives updates from C and D. Cost of link=1. What is new cost and next hop for Z from A?", "options": ["a) 8, B", "b) 6, C", "c) 9, D", "d) 7, C"], "answer": "d) 7, C", "solution": "Cost(Z from A) = Cost(Z from C) + Cost(C from A) = 6 + 1 = 7."}
    ],
    "Week 9": [
        {"question": "1. Which component of SDN is responsible for communicating with the controller?", "options": ["a) Data plane", "b) Control plane", "c) Management plane", "d) Forwarding plane"], "answer": "b) Control plane", "solution": "The control plane communicates with the controller to manage traffic flow."},
        {"question": "2. A subset of a network that includes all the routers but contains no loops is called", "options": ["a) Spanning tree", "b) Spider structure", "c) Spider tree", "d) Special tree"], "answer": "a) Spanning tree", "solution": "Spanning Tree Protocol creates a loop-free logical topology."},
        {"question": "3. Which classes are used for connection-less socket programming?", "options": ["a) Datagram Socket", "b) Datagram Packet", "c) Both Datagram Socket & Datagram Packet", "d) Server Socket"], "answer": "c) Both Datagram Socket & Datagram Packet", "solution": "Datagram Socket and Datagram Packet are used for connection-less sockets (UDP)."},
        {"question": "4. Which of the following is NOT a function of a router?", "options": ["a) Path determination", "b) Packet forwarding", "c) Packet filtering", "d) Packet retransmission"], "answer": "d) Packet retransmission", "solution": "Packet retransmission is a transport layer (TCP) function, not a router function."},
        {"question": "5. What is the role of the OpenFlow protocol in SDN?", "options": ["a) To enable communication between the control plane and data plane", "b) Encryption", "c) Monitor performance", "d) Manage security"], "answer": "a) To enable communication between the control plane and data plane", "solution": "OpenFlow enables communication between control plane and data plane."},
        {"question": "6. Which type of Ethernet framing is used for TCP/IP and DEC net?", "options": ["a) Ethernet 802.3", "b) Ethernet 802.2", "c) Ethernet II", "d) Ethernet SNAP"], "answer": "c) Ethernet II", "solution": "Ethernet II is used with TCP/IP and DEC net."},
        {"question": "7. Which of the following is not true regarding Forward Information Base (FIB)?", "options": ["a) Mirrors RIB", "b) Responsible for merging the data plane and control plane together", "c) Routing decisions from FIB", "d) Stored in TCAM"], "answer": "b) Responsible for merging the data plane and control plane together", "solution": "FIB allows Data and Control plane to be SEPARATED, not merged."},
        {"question": "8. What is the role of the northbound interface in SDN?", "options": ["a) Configure devices", "b) To enable communication between the controller and applications", "c) Monitor traffic", "d) Provide services to end users"], "answer": "b) To enable communication between the controller and applications", "solution": "Northbound interface connects the controller and higher-level applications."},
        {"question": "9. A network 192.168.10.0/24 needs at least 12 subnets. Which subnet mask should be used?", "options": ["a) 255.255.255.224", "b) 255.255.255.240", "c) 255.255.255.192", "d) 255.255.255.248"], "answer": "b) 255.255.255.240", "solution": "2^4 = 16 subnets (borrow 4 bits). Prefix becomes /28 = 255.255.255.240."},
        {"question": "10. True regarding: ip route 172.16.4.0 255.255.255.0 192.168.4.2?", "options": ["a) I and II", "b) II and IV", "c) III and IV", "d) I, II, III and IV"], "answer": "a) I and II", "solution": "It establishes a static route (I) and uses the default administrative distance of 1 (II). The mask is for the remote network, not source."}
    ],
    "Week 10": [
        {"question": "1. Which is NOT one of the LLC services?", "options": ["a) Connection mode service", "b) Acknowledged connectionless service", "c) Intermediate switching service", "d) Unacknowledged connectionless service"], "answer": "c) Intermediate switching service", "solution": "Intermediate switching service is not defined as an LLC service."},
        {"question": "2. IEEE 802.1 is concerned with which issue in LANs and MANS?", "options": ["a) Error handling", "b) Networking", "c) Internetworking", "d) Flow control"], "answer": "c) Internetworking", "solution": "IEEE 802.1 deals with internetworking issues in LANs and MANs (bridging, VLANs)."},
        {"question": "3. Which sublayer of the data link layer performs data link functions that depend upon the type of medium?", "options": ["a) Logical link control sublayer", "b) Media access control sublayer", "c) Network interface control sublayer", "d) Error control sublayer"], "answer": "b) Media access control sublayer", "solution": "The MAC sublayer handles functions depending on the physical transmission medium."},
        {"question": "4. In 10Base-T and 100Base-T Ethernet technology, what does the letter 'T' represent?", "options": ["a) Transmission", "b) Twisted Pair", "c) Total utilization", "d) Top Speed"], "answer": "b) Twisted Pair", "solution": "T stands for Twisted Pair copper cables."},
        {"question": "5. In Go-Back-N ARQ, if the window size is 63, what is the range of sequence numbers?", "options": ["a) 1 to 63", "b) 1 to 64", "c) 0 to 63", "d) 0 to 64"], "answer": "c) 0 to 63", "solution": "Range is 0 to (2^m - 1). For window size 63, range is 0 to 63."},
        {"question": "6. When 2 or more bits in a data unit have been changed during the transmission, the error is called", "options": ["a) Random error", "b) Burst error", "c) Inverted error", "d) Double error"], "answer": "b) Burst error", "solution": "When more than a single bit is corrupted, it is a burst error."},
        {"question": "7. Which of the following are correct about Asynchronous MAC techniques?\nI. Reservation method suited for streaming voice traffic.\nII. Contention method suitable for continuous traffic.", "options": ["a) Only I", "b) Only II", "c) Both I and II", "d) Neither I nor II"], "answer": "a) Only I", "solution": "Reservation method is good for continuous/real-time traffic. Contention is for bursty traffic."},
        {"question": "8. Pure ALOHA network transmits 200 bit frames at 200 kbps. System generates 250 frames per second. What is throughput?", "options": ["a) 38 frames", "b) 48 frames", "c) 96 frames", "d) 126 frames"], "answer": "a) 38 frames", "solution": "G = 1/4. Throughput = 250 * [G * e^(-2G)] = 250 * 0.152 = 38 frames."},
        {"question": "9. Which of the following is/are true?\nI. Full-duplex switched Ethernet, no need for CSMA/CD.\nIV. Random backoff in CSMA/CD reduces probability of retransmitting at same time.", "options": ["a) I and IV", "b) I and III", "c) II and III", "d) II and IV"], "answer": "a) I and IV", "solution": "Collisions don't occur in full-duplex (I is true). Random backoff prevents repeated collisions (IV is true)."},
        {"question": "10. CSMA/CD bandwidth 10 Mbps. Max propagation delay 25.6 us. Minimum frame size?", "options": ["a) 128 bytes", "b) 32 bytes", "c) 16 bytes", "d) 64 bytes"], "answer": "d) 64 bytes", "solution": "Min frame transmission time = 2 * 25.6 = 51.2 us. Size = 51.2 us * 10 Mbps = 512 bits = 64 bytes."}
    ],
    "Week 11": [
        {"question": "1. Which of the following addresses is used in Ethernet broadcast for ARP requests?", "options": ["a) 255.255.255.255", "b) 255.255.255.254", "c) FF:FF:FF:FF:FF:FF", "d) 255.255.255.251"], "answer": "c) FF:FF:FF:FF:FF:FF", "solution": "ARP requests use the broadcast MAC address FF:FF:FF:FF:FF:FF."},
        {"question": "2. Which field in an ARP packet is not filled in ARP Request but filled in ARP Reply?", "options": ["a) Target protocol address", "b) Target hardware address", "c) Sender protocol address", "d) Sender hardware address"], "answer": "b) Target hardware address", "solution": "The target hardware address is unknown in the request and filled in the reply."},
        {"question": "3. Which protocol does DHCP use at the Transport layer?", "options": ["a) IP", "b) ARP", "c) UDP", "d) TCP"], "answer": "c) UDP", "solution": "DHCP uses UDP (ports 67 and 68)."},
        {"question": "4. Which of the following is/are correct about RARP?", "options": ["a) RARP replies are broadcast.", "b) RARP is often used on thin-client workstations.", "c) Sender hardware address field is not filled.", "d) RARP has been replaced by DHCP."], "answer": "b, d", "solution": "RARP replies are unicast. It was used by thin clients and replaced by DHCP."},
        {"question": "5. To deal with hidden terminal and exposed station problems, 802.11 WLAN must mandatorily support", "options": ["a) DCF", "b) PCF", "c) Both are mandatory", "d) Both are optional"], "answer": "a) DCF", "solution": "DCF (Distributed Coordination Function) is mandatory in 802.11."},
        {"question": "6. When a new trunk link is configured on an IOS-based switch, which VLANs are allowed over the link?", "options": ["a) By default, all VLANs are allowed on the trunk.", "b) No VLAN's are allowed", "c) Only configured VLAN's", "d) Only extended VLAN's"], "answer": "a) By default, all VLANs are allowed on the trunk.", "solution": "On IOS-based switches, all VLANs are allowed by default on a trunk."},
        {"question": "7. Which VLAN technique is used when a single link needs to carry traffic for multiple VLANs?", "options": ["a) Tailing", "b) Trunking", "c) Trading", "d) Tapping"], "answer": "b) Trunking", "solution": "Trunking carries multiple VLAN traffic over a single physical link."},
        {"question": "8. What type of interface is necessary on the router if only one connection is made between the router and the switch for inter-VLAN?", "options": ["a) 10Mbps Ethernet", "b) 56Kbps Serial", "c) 100Mbps Ethernet", "d) 1Gbps Ethernet"], "answer": "c) 100Mbps Ethernet", "solution": "A 100 Mbps Ethernet is the minimum suitable for 'router-on-a-stick' trunking."},
        {"question": "9. Which specifies a set of MAC and physical layer specifications for implementing WLANs?", "options": ["a) IEEE 802.16", "b) IEEE 802.3", "c) IEEE 802.11", "d) IEEE 802.15"], "answer": "c) IEEE 802.11", "solution": "IEEE 802.11 is the specification for WLANs."},
        {"question": "10. LAN 100 hosts, each sends ARP request every 10 seconds. Packet is 64 bytes. Total ARP traffic per second?", "options": ["a) 320 bytes/sec", "b) 640 bytes/sec", "c) 1280 bytes/sec", "d) 6400 bytes/sec"], "answer": "b) 640 bytes/sec", "solution": "100 hosts / 10 sec = 10 packets/sec. 10 * 64 bytes = 640 bytes/sec."}
    ],
    "Week 12": [
        {"question": "1. If there are n signal sources, each transmitting at the same data rate, how many time slots are required in a Time Division Multiplexing (TDM) link?", "options": ["a) n/2", "b) 2n", "c) n", "d) n^2"], "answer": "c) n", "solution": "Correct Option is (c). n time slots are required."},
        {"question": "2. Suppose we have a HDTV screen with screen resolution 1600x1200 and the screen is renewed 50 times per second. Considering a colored pixel needs 24 bits, what is the bit rate?", "options": ["a) 1.3 Gbps", "b) 2.3 Gbps", "c) 3.3 Gbps", "d) 4.3 Gbps"], "answer": "b) 2.3 Gbps", "solution": "Correct Option is (b)."},
        {"question": "3. A composite signal contains frequencies 300, 500, 800, 1000 and 1500 Hz. What is the bandwidth?", "options": ["a) 1000 Hz", "b) 200 Hz", "c) 1200 Hz", "d) 500 Hz"], "answer": "c) 1200 Hz", "solution": "Bandwidth is highest frequency minus lowest frequency: 1500 - 300 = 1200 Hz."},
        {"question": "4. Which component is included in IP security?", "options": ["a) Authentication Header (AH)", "b) Encapsulating Security Payload (ESP)", "c) Internet key Exchange (IKE)", "d) All of the mentioned"], "answer": "d) All of the mentioned", "solution": "IPSec includes AH, ESP, and IKE."},
        {"question": "5. Which of the following is NOT a cause of transmission impairment?", "options": ["a) Attenuation", "b) Noise", "c) Distortion", "d) Congestion"], "answer": "d) Congestion", "solution": "Congestion is a network traffic issue, not a physical transmission impairment like noise or attenuation."},
        {"question": "6. Which of the following is/are NOT true about modulation techniques?", "options": ["a) One amplitude in ASK is zero.", "b) BFSK is more susceptible to error than ASK.", "c) In Binary PSK, presence and absence of the carrier signal represents two binary digits.", "d) QAM is a combination of ASK and PSK"], "answer": "c) In Binary PSK, presence and absence of the carrier signal represents two binary digits.", "solution": "In BPSK, phase shifts represent the digits, not the presence/absence of the carrier signal."},
        {"question": "7. Which of the following attacks can actively modify communications or data?", "options": ["a) Both active and passive attacks", "b) Neither active and passive attacks", "c) Active attacks", "d) Passive attacks"], "answer": "c) Active attacks", "solution": "Active attacks modify data, while passive attacks only monitor or eavesdrop."},
        {"question": "8. Which one is used in parts of the cellular telephone system and for some satellite communication?", "options": ["a) CDM", "b) TDM", "c) FDM", "d) WDM"], "answer": "a) CDM", "solution": "CDM (Code Division Multiplexing) is heavily used in cellular and satellite systems."},
        {"question": "9. Which of the following statements is/are correct?\n(a) NAT is a proxy server\n(b) NAT can also act as a firewall.\n(c) NAT needs to recalculate both IP and TCP checksum...\n(d) IP masquerading is done by NAT.", "options": ["a) Only a", "b) b, c, d", "c) a, b, c", "d) Only d"], "answer": "b) b, c, d", "solution": "NAT masquerades IP addresses, acts as a basic firewall, and recalculates checksums after modification."},
        {"question": "10. If the frequency spectrum of a signal has a bandwidth of 500 Hz with the highest frequency at 600 Hz, what should be the sampling rate according to the Nyquist theorem?", "options": ["a) 200 samples/sec", "b) 500 samples/sec", "c) 1000 samples/sec", "d) 1200 samples/sec"], "answer": "d) 1200 samples/sec", "solution": "Nyquist theorem: sampling rate must be at least 2 * highest frequency. 2 * 600 = 1200 samples/sec."}
    ]
}

# ==========================================
# PAGE ROUTING
# ==========================================

# --- HOME PAGE ---
if st.session_state.page == 'home':
    st.markdown("<div class='portal-header'>CNIP Quiz Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='portal-sub'>Computer Networks & Internet Protocol</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    weeks = list(quiz_data.keys())
    
    for i, week in enumerate(weeks):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(f"""
            <div class='week-card'>
                <div style='color:#1e3a8a; font-size:0.85rem; font-weight:bold; letter-spacing: 1px;'>{week.upper()}</div>
                <div class='week-title'>Assignment: Computer Networks</div>
                <div style='color:#64748b; font-size:0.9rem; margin-bottom: 12px;'>{len(quiz_data[week])} Questions</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Start {week} Quiz", key=f"start_{week}", type="primary"):
                start_quiz(week)
                st.rerun()

    st.write("---")
    
    _, mid_col, _ = st.columns([1, 2, 1])
    with mid_col:
        st.markdown(f"""
        <div class='week-card' style='text-align: center; border: 1px solid #10b981;'>
            <div style='color:#065f46; font-size:0.85rem; font-weight:bold; letter-spacing: 1px;'>GRAND FINALE</div>
            <div class='week-title'>Comprehensive Final Exam</div>
            <div style='color:#64748b; font-size:0.9rem; margin-bottom: 12px;'>Test your knowledge with all 120 questions.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start 120-Question Final Exam", key="start_final", type="primary"):
            start_quiz("Final Exam")
            st.rerun()

# --- WEEKLY QUIZ PAGE (PAGINATED WITH INSTANT FEEDBACK) ---
elif st.session_state.page == 'quiz':
    week = st.session_state.current_week
    questions = quiz_data[week]
    idx = st.session_state.q_index
    q = questions[idx]
    
    # Top Bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"<div class='quiz-title'>{week} Assignment</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='question-count'>Question {idx + 1} of {len(questions)}</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Back to Home", key="btn_home", type="primary"):
            change_page('home')
            st.rerun()
    with col3:
        if st.button("End Test", key="btn_end", type="primary"):
            change_page('results')
            st.rerun()
            
    # Progress Bar
    progress = (idx + 1) / len(questions)
    st.progress(progress)
    st.write("---")
    
    # Question & Options
    st.markdown(f"**{q['question']}**")
    saved_ans = st.session_state.user_answers.get(idx, None)
    selected_option = st.radio("Select an option:", q["options"], index=q["options"].index(saved_ans) if saved_ans else None, label_visibility="collapsed")
    
    # INSTANT FEEDBACK LOGIC
    if selected_option:
        st.session_state.user_answers[idx] = selected_option
        if selected_option == q["answer"]:
            st.markdown(f"<div class='ans-correct'>✓ Correct!</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ans-wrong'>✗ Incorrect.<br><br><b>Correct Answer:</b> {q['answer']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='explanation'><b>Explanation:</b> {q['solution']}</div>", unsafe_allow_html=True)

    st.write("---")
    
    # Bottom Navigation
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if idx > 0:
            if st.button("Previous"): 
                prev_question()
                st.rerun()
    with nav_col3:
        if idx < len(questions) - 1:
            if st.button("Next", type="primary"): 
                next_question()
                st.rerun()
        else:
            if st.button("Submit Exam", type="primary"): 
                change_page('results')
                st.rerun()

# --- FINAL EXAM PAGE (ALL 120 QUESTIONS WITH INSTANT FEEDBACK) ---
elif st.session_state.page == 'final_exam':
    all_questions = [q for week in quiz_data.values() for q in week]
    
    # Top Bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='quiz-title'>Comprehensive Final Exam</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='question-count'>All {len(all_questions)} Questions</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Back to Home", key="btn_home_final", type="primary"):
            change_page('home')
            st.rerun()
            
    st.write("---")
    
    # Loop for 120 questions (Instant Feedback added, Form removed)
    for i, q in enumerate(all_questions):
        st.markdown(f"**Question {i + 1}: {q['question'].split('.', 1)[-1].strip()}**")
        saved_ans = st.session_state.user_answers.get(i, None)
        
        # Unique key for each radio button
        selected_option = st.radio("Options", q['options'], key=f"fq_{i}", index=q['options'].index(saved_ans) if saved_ans else None, label_visibility="collapsed")
        
        # INSTANT FEEDBACK LOGIC
        if selected_option:
            st.session_state.user_answers[i] = selected_option
            if selected_option == q["answer"]:
                st.markdown(f"<div class='ans-correct'>✓ OHHH YES, PUSH MORE HARDER!</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ans-wrong'>✗ OHHH NO.<br><br><b>Correct Answer:</b> {q['answer']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='explanation'><b>Explanation:</b> {q['solution']}</div>", unsafe_allow_html=True)
            
        st.write("---")
        
    if st.button("Submit Final Exam", type="primary"):
        change_page('final_results')
        st.rerun()
