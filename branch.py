import grpc
import branch_pb2
import branch_pb2_grpc
import json
from customer import Customer
from concurrent import futures
import multiprocessing
import time
import sys
import operator


class Branch(branch_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()

        # store processID of the branches
        self.processID = list()

        self.writeset = list()


    # execute the transactions
    def executeMessage(self, request, updateBranches):


        #self.processID.append(str(request.id))

        if request.interface == "query":
            pass



        # handle deposit and propagation
        elif request.interface == "deposit":
            self.balance += request.money
            if updateBranches:
                self.Propagate_Deposit(request)

        # handle withdraw and propagation
        elif request.interface == "withdraw" and self.balance >= request.money:
            self.balance -= request.money
            if updateBranches:
                self.Propagate_Withdraw(request)
        if request.interface != "query":
            self.UpdateWriteSet()



        return branch_pb2.MsgResponse(interface=request.interface, money=self.balance, writeset = self.writeset)


    # propagate withdraw
    def Propagate_Withdraw(self, request):
        for x in self.stubList:
            x.MsgPropagation(branch_pb2.MsgRequest(interface="withdraw", money=request.money, writeset=self.writeset))

    # propagate deposit
    def Propagate_Deposit(self, request):
        for y in self.stubList:
            y.MsgPropagation(branch_pb2.MsgRequest(interface="deposit", money=request.money, writeset=self.writeset))

    # validate writesets are consistent
    def Validate(self,data):
        return self.writeset==data

    # update the branch writeset
    def UpdateWriteSet(self):
        ID = len(self.writeset)+1
        self.writeset.append(ID)


    # process messages from customers
    def MsgDelivery(self, request, context):

        while  self.Validate(request.writeset)==False:

            time.sleep(0.1)
        return self.executeMessage(request, True)

    # process propagation
    def MsgPropagation(self, request, context):

        while  self.Validate(request.writeset)==False:
            time.sleep(0.1)
        return self.executeMessage(request, False)

    # generate branch stubs
    def createBranchStubs(self):
        for ID in self.branches:
            if ID != self.id:
                port = str(50000 + ID)
                channel = grpc.insecure_channel("localhost:" + port)
                self.stubList.append(branch_pb2_grpc.BranchStub(channel))

# start the branch server and stubs
def executeBranch(branch):
    branch.createBranchStubs()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    branch_pb2_grpc.add_BranchServicer_to_server(branch, server)
    port = str(50000 + branch.id)
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


# start the customer stubs and execute events
def executeCustomer(customer, output):
    #customer.createStub()
    customer.executeEvents()

    output.append(customer.output())

#execute the data from the input file and starts the execution of the program using multiprocessing
def execute(branchList, customerList):
    #lists to store branch and customer objects and processes

    branchExecutionList = []

    customerExecutionList = []


    manager = multiprocessing.Manager()
    output = manager.list()


    # multiprocessing of branches
    for branch in branchList:
        branchProcess = multiprocessing.Process(target=executeBranch, args=(branch,))
        branchExecutionList.append(branchProcess)
        branchProcess.start()

    # time to allow for all branches to start
    time.sleep(5)

    # multiprocessing of customers
    for customer in customerList:
        customerProcess = multiprocessing.Process(target=executeCustomer, args=(customer, output,))
        customerExecutionList.append(customerProcess)
        customerProcess.start()

    # ensure all customer events are completed
    for customerProcess in customerExecutionList:
        customerProcess.join()

    # branches are terminated
    for branchProcess in branchExecutionList:
        branchProcess.terminate()



    # final output is written to file
    #finalOutput = sorted(output, key=operator.itemgetter('id'))
    for i in output:
        outputFile.write(str(i) + "\n")





# main function handles input file
if __name__ == "__main__":
    branchList = []
    branchIDList = []

    customerList = []




    filename = sys.argv[-1]
    file = open(filename)
    output = str(filename[:-5])+"Output.txt"
    outputFile = open(output, "w")
    input = json.load(file)

    # generate branch and customer objects based on the data in the input file
    for actions in input:
        if actions["type"] == "branch":
            branch = Branch(actions["id"], actions["balance"], branchIDList)
            branchList.append(branch)
            branchIDList.append(branch.id)

        elif actions["type"] == "customer":
            customer = Customer(actions["id"], actions["events"])
            customerList.append(customer)

    execute(branchList, customerList)

    outputFile.close()



