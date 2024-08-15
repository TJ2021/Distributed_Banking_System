import grpc
import branch_pb2
import branch_pb2_grpc
import time

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        self.writeset = list()


    # generates customer stubs
    # def createStub(self):
    #     port = str(50000 + self.id)
    #     channel = grpc.insecure_channel("localhost:" + port)
    #     self.stub = branch_pb2_grpc.BranchStub(channel)
    #

    # send events to branches
    def executeEvents(self):
        for event in self.events:

            port = str(50000 + event["dest"])
            channel = grpc.insecure_channel("localhost:" + port)
            self.stub = branch_pb2_grpc.BranchStub(channel)

            money = event["money"] if event["interface"] != "query" else 0

            # request to branch server
            response = self.stub.MsgDelivery(branch_pb2.MsgRequest(interface=event["interface"], money=money, writeset=self.writeset))

            message = {"interface": response.interface, "dest": event["dest"],"money":response.money}

            self.recvMsg.append(message)

            if event["interface"]!="query":
                self.writeset= response.writeset

            time.sleep(3)

    # generate output message
    def output(self):
        return {"id": self.id, "balance": self.recvMsg[-1]["money"]}
