import os
import peewee
import datetime

import threading


try:
    import Queue
except ImportError:
    import queue as Queue


temp_storeModels_Folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "//"
TempBaseDBName = "PeeWee_Temp_PrivateReceiverRequests_DB"


class StoreModelHeader(object):

    def __init__(self):
        self.db_name = TempBaseDBName + ".db"

        self.db = None

        self._pre_refresh()

    def _pre_refresh(self):
        self._pre_refresh_dbPath()
        self._pre_refresh_access()

    def _pre_refresh_dbPath(self):
        FolderPath = temp_storeModels_Folder  # os.path.expanduser(os.path.join(DBPath, str(TempBaseDBName)))

        if not os.path.exists(os.path.dirname(FolderPath)):
            os.makedirs(os.path.dirname(FolderPath))

        self.db_path = os.path.expanduser(os.path.join(FolderPath, str(self.db_name)))

    def _pre_refresh_access(self):
        self.is_inUsing_internal = False

        self.access_using_Lock = threading.Lock()
        self._check_inUsing_Lock = threading.Lock()

    def open_using(self):
        self.access_using_Lock.acquire()

    def close_using(self):
        self.access_using_Lock.release()

    def set_db(self, db):
        self.db = db


class ReceiverRequestsPrivateStoreModel(object):

    def __init__(self):

        self.storeModelHeader = StoreModelHeader()
        #
        self.storeModelHeader.open_using()

        self.databasePath = self.storeModelHeader.db_path

        self.db = peewee.SqliteDatabase(self.databasePath)
        self.is_connect = False

        # self.db.connect()
        self.connect_db()

        class BaseModel(peewee.Model):

            def save_toQueue(objectModel):
                self.saveQueue_tempRepostery.put(objectModel)

                if not self.saveQueue_isLoopRunning:
                    threading.Thread(target=self.runSaveQueue).start()

            class Meta:
                database = self.db

        ################# Receiver Models ###################
        class HandleRequestState:

            unknown = "unknown"
            JustAdd = "just_add"
            processorAck = "processor-ack"

            processedBase = "processed_base"
            underProcessing = "under_processing"
            startProcessing = "start_processing"
            cancled = "cancled"
            doneSending = "done_sending"
            dateOut = "dateOut"

            HandleRequestStates_list = [
                unknown,
                JustAdd,
                processorAck,

                processedBase,
                underProcessing,
                startProcessing,
                cancled,
                doneSending,
                dateOut
            ]

            HANDLE_REQUEST_STATE = (
                (unknown, "unknown"),
                (JustAdd, "just_add"),
                (processorAck, "processor-ack"),


                (processedBase, "processed_base"),
                (underProcessing, "under_processing"),
                (startProcessing, "start_processing"),
                (cancled, "cancled"),
                (doneSending, "done_sending"),
                (dateOut, "dateOut"),
            )

        self.HandleRequestState = HandleRequestState

        class HandleRequestType:

            unknown = "unknown"
            client = "client"
            sys = "sys"

            HandleRequestTypes_list = [
                unknown,
                client,
                sys
            ]

            HANDLE_REQUEST_TYPE = (
                (unknown, "unknown"),
                (client, "client"),
                (sys, "sys"),
            )

        self.HandleRequestType = HandleRequestType


        class UserProcessorHandleRequest(BaseModel):
            id = peewee.AutoField(primary_key=True)

            request_state = peewee.CharField(null=True, choices=HandleRequestState.HANDLE_REQUEST_STATE,
                                              default=HandleRequestState.JustAdd)
            request_id = peewee.CharField(null=True)
            request_num = peewee.CharField(null=True)

            user_objectId = peewee.CharField(null=True)
            processor_objectId = peewee.CharField(null=True)

            row_data = peewee.TextField(null=True)
            result_data = peewee.TextField(null=True)

            added = peewee.DateTimeField(default=datetime.datetime.now)

            class Meta:
                db_table = 'at_user_processor_handle_requests'

        self.UserProcessorHandleRequest = UserProcessorHandleRequest

        ########################### db tables ################################

        self.db.create_tables(
            [
                UserProcessorHandleRequest,
            ])

        ############################ Lock_s ################################

        self.main_using_Lock = threading.Lock()
        self.is_store_in_using = False
        self.waitting_mainUsingLock = threading.Lock()

        self.mainSelectLock = threading.Lock()

        ################### Threads Info ###########

        ####### saveQueue Threads ######
        self.saveQueue_tempRepostery = Queue.Queue(1000)
        self.saveQueue_queueLock = threading.Lock()
        self.saveQueue_isLoopRunning = False

        ################### Threads Info ###########
        self.openOper_Lock = threading.Lock()

        #
        self.storeModelHeader.close_using()

    def runSaveQueue(self):
        self.saveQueue_isLoopRunning = True

        ## open_oper
        self.open_oper()
        self.mainSelectLock.acquire()

        while not self.saveQueue_tempRepostery.empty():
            self.saveQueue_queueLock.acquire()

            self.saveQueue_tempRepostery.get().save()

            try:
                pass
            except:
                print("\nTempContactsStoreModel : runSaveQueue : error")

            self.saveQueue_queueLock.release()

        self.mainSelectLock.release()

        self.saveQueue_isLoopRunning = False

        ## close_oper
        self.close_oper()

    def open_using(self):

        self.waitting_mainUsingLock.acquire()

        while self.is_store_in_using:
            continue

        self.is_store_in_using = True

        self.waitting_mainUsingLock.release()

        self.main_using_Lock.acquire()

    def close_using(self):

        self.is_store_in_using = False
        self.main_using_Lock.release()

    def open_oper(self):
        self.storeModelHeader.open_using()
        self.openOper_Lock.acquire()

    def close_oper(self):
        self.storeModelHeader.close_using()
        self.openOper_Lock.release()

    # --------------------- For Connection -----------------------#

    def connect_db(self):
        self.db.connect()
        self.is_connect = True

    def dis_connect_db(self):
        pass
        self.db.close()
        self.is_connect = False




























