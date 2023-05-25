import aiohttp
import xml.etree.ElementTree as ET

class MessagingAPI:
    wsdl_url = None
    namespace = None

    def __init__(self, app, app_url):
        match app.lower():
            case "pc": 
                self.wsdl_url = app_url+'/ws/gw/webservice/pc/MessagingToolsAPI?WSDL'
                self.namespace = "http://guidewire.com/pc/ws/gw/webservice/pc/MessagingToolsAPI"
            case "bc": 
                self.wsdl_url = app_url+'/ws/gw/webservice/bc/MessagingToolsAPI?WSDL'
                self.namespace = "http://guidewire.com/bc/ws/gw/webservice/bc/MessagingToolsAPI"
            case "cc": 
                self.wsdl_url = app_url+'/ws/gw/webservice/cc/MessagingToolsAPI?WSDL'
                self.namespace = "http://guidewire.com/cc/ws/gw/webservice/cc/MessagingToolsAPI"
            case "ab": 
                self.wsdl_url = app_url+'/ws/gw/webservice/ab/MessagingToolsAPI?WSDL'
                self.namespace = "http://guidewire.com/ab/ws/gw/webservice/ab/MessagingToolsAPI"
            case __: raise Exception("Inavalid app")

    async def is_suspended(self, mq_id):
        async with aiohttp.ClientSession() as session:
            is_suspended_payload = '''
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:soap1="http://guidewire.com/ws/soapheaders" xmlns:mes="'''+self.namespace+'''">
            <soap:Header>
                <soap1:authentication>
                    <soap1:username>su</soap1:username>
                    <soap1:password>gw</soap1:password>
                </soap1:authentication>
            </soap:Header>
            <soap:Body>
                <mes:isSuspended>
                    <mes:destID>'''+str(mq_id)+'''</mes:destID>
                </mes:isSuspended>
            </soap:Body>
            </soap:Envelope>
            '''
            async with session.post(self.wsdl_url, data=is_suspended_payload, headers={'SOAPAction': 'isSuspended'}) as response:
                response_content = await response.content.read()
                status_code = response.status
                if(status_code < 300):
                    root = ET.fromstring(response_content)
                    result = root.find('.//ns:return', {'ns': self.namespace}).text
                    return True if result == "true" else False
                else:
                    raise Exception("Unreachable")

    async def is_resumed(self, mq_id):
        async with aiohttp.ClientSession() as session:
            is_resumed_payload = '''
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:soap1="http://guidewire.com/ws/soapheaders" xmlns:mes="'''+self.namespace+'''">
            <soap:Header>
                <soap1:authentication>
                    <soap1:username>su</soap1:username>
                    <soap1:password>gw</soap1:password>
                </soap1:authentication>
            </soap:Header>
            <soap:Body>
                <mes:isResumed>
                    <mes:destID>'''+str(mq_id)+'''</mes:destID>
                </mes:isResumed>
            </soap:Body>
            </soap:Envelope>
            '''
            async with session.post(self.wsdl_url, data=is_resumed_payload, headers={'SOAPAction': 'isResumed'}) as response:
                response_content = await response.content.read()
                status_code = response.status
                if(status_code < 300):
                    root = ET.fromstring(response_content)
                    result = root.find('.//ns:return', {'ns': self.namespace}).text
                    return True if result == "true" else False
                else:
                    raise Exception("Unreachable")

    async def resume(self, mq_id):
        async with aiohttp.ClientSession() as session:
            resume_destination_payload = '''
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:soap1="http://guidewire.com/ws/soapheaders" xmlns:mes="'''+self.namespace+'''">
            <soap:Header>
                <soap1:authentication>
                    <soap1:username>su</soap1:username>
                    <soap1:password>gw</soap1:password>
                </soap1:authentication>
            </soap:Header>
            <soap:Body>
                <mes:resumeDestinationBothDirections>
                    <mes:destID>'''+str(mq_id)+'''</mes:destID>
                </mes:resumeDestinationBothDirections>
            </soap:Body>
            </soap:Envelope>
            '''
            async with session.post(self.wsdl_url, data=resume_destination_payload, headers={'SOAPAction': 'resumeDestinationBothDirections'}) as response:
                await response.content.read()
                status_code = response.status
                return status_code < 300