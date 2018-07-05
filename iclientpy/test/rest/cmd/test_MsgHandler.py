from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.rest.cmd.imgrwxreceiver import MsgHandler
from iclientpy.dtojson import deserializer
from iclientpy.rest.api.model import NodeInfoList,BatchMethodResult
from iclientpy.rest.api.node_service import NodeService

class MsgHandlerTest(TestCase):
    _node_s: NodeService
    def setUp(self):
        self._node_s = MagicMock()
        factory = MagicMock()
        factory.node_service = MagicMock(return_value=self._node_s)
        factory_kls = MagicMock(return_value=factory)
        self._msg_handler = MsgHandler('http://imgr.supermap.io/imanager','user', 'password', factory_kls)

    def test_help(self):
        self.assertEqual(self._msg_handler('lsit'), 'list/stop {id}/start {id}')

    def test_list(self):
        json_str = '{"list":[{"address":"http://123.56.45.215:62463/iserver","dbs":[],"hasAgent":false,"id":6,"isCreate":true,"isMonitored":true,"name":"地图服务","owner":"admin","status":[],"type":"iServer"},{"address":"http://123.56.45.215:16562/iportal","dbs":[],"hasAgent":false,"id":10,"isCreate":true,"isMonitored":true,"name":"GIS门户","owner":"admin","status":[],"type":"iPortal"}],"total":2}'
        node_list = deserializer(NodeInfoList)(json_str)
        self._node_s.get_services = MagicMock(return_value = node_list)
        self._node_s.get_current_M_PortTCP = MagicMock(side_effect  =[{'value':'1'},{'value':'0'}])
        result = self._msg_handler('list')
        self.assertIn('6：地图服务(iServer)-在线', result)
        self.assertIn('10：GIS门户(iPortal)-离线', result)

    def test_stop(self):
        result = BatchMethodResult()
        result.isSucceed = True
        self._node_s.stop_nodes = MagicMock(return_value = result)
        self.assertEqual(self._msg_handler('stop 6'), '停止6成功')

        result = BatchMethodResult()
        result.isSucceed = False
        self._node_s.stop_nodes = MagicMock(return_value = result)
        self.assertEqual(self._msg_handler('stop 6'), '停止6失败')

    def test_startp(self):
        result = BatchMethodResult()
        result.isSucceed = True
        self._node_s.start_nodes = MagicMock(return_value = result)
        self.assertEqual(self._msg_handler('start 6'), '启动6成功')

        result = BatchMethodResult()
        result.isSucceed = False
        self._node_s.start_nodes = MagicMock(return_value = result)
        self.assertEqual(self._msg_handler('start 6'), '启动6失败')