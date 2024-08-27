# Distributed Banking System
## About The Project
The Distributed Banking System is an application designed to handle transactions across multiple bank branches in a distributed environment.
Utilizing gRPC for communication, the system ensures consistency and reliability in managing deposits, withdrawals, and balance queries. 
The project leverages the concept of distributed computing to simulate the operations of a banking network, where each branch operates independently yet stays synchronized with others.
The system is built to handle simultaneous client requests and propagate updates across all branches, ensuring data integrity and consistency.<br><br>

### Features
- Distributed Branch Operations: Each branch operates independently, handling its transactions while maintaining consistency with other branches.
- Transaction Propagation: Deposits and withdrawals made at one branch are propagated to other branches, ensuring that the system remains synchronized.
- Balance Queries: Clients can query their balance at any branch, with the system ensuring that the most up-to-date information is retrieved.

### Built With
- Python
- gRPC<br><br>

## Lessons Learned
- Enhanced Skills in gRPC and Distributed Systems: Gained practical experience in implementing and managing a distributed system using gRPC, ensuring reliable communication between multiple processes.
- Deepened Understanding of Consistency Mechanisms: Developed a stronger grasp of consistency models in distributed systems, particularly the importance of write-set validation to maintain data integrity.


