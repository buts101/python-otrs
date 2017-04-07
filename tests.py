import unittest
import os
import xml.etree.ElementTree as etree

from otrs.client import GenericInterfaceClient
from otrs.ticket.template import GenericTicketConnectorSOAP
from otrs.ticket.objects import Ticket, Article

REQUIRED_VARS = 'OTRS_LOGIN', 'OTRS_PASSWORD', 'OTRS_SERVER', 'OTRS_WEBSERVICE'
MISSING_VARS = []

for i in REQUIRED_VARS:
    if not i in os.environ.keys():
        MISSING_VARS.append(i)
    else:
        (locals())[i] = os.environ[i]

SAMPLE_TICKET = """<Ticket>
            <Age>346654</Age>
            <ArchiveFlag>n</ArchiveFlag>
            <ChangeBy>2</ChangeBy>
            <Changed>2014-05-16 11:24:19</Changed>
            <CreateBy>1</CreateBy>
            <CreateTimeUnix>1400234702</CreateTimeUnix>
            <Created>2014-05-16 10:05:02</Created>
            <CustomerID>1001</CustomerID>
            <CustomerUserID>user1</CustomerUserID>
            <EscalationResponseTime>0</EscalationResponseTime>
            <EscalationSolutionTime>0</EscalationSolutionTime>
            <EscalationTime>0</EscalationTime>
            <EscalationUpdateTime>0</EscalationUpdateTime>
            <GroupID>1</GroupID>
            <Lock>unlock</Lock>
            <LockID>1</LockID>
            <Owner>fbarman</Owner>
            <OwnerID>2</OwnerID>
            <Priority>3 normal</Priority>
            <PriorityID>3</PriorityID>
            <Queue>Support</Queue>
            <QueueID>2</QueueID>
            <RealTillTimeNotUsed>0</RealTillTimeNotUsed>
            <Responsible>admin</Responsible>
            <ResponsibleID>1</ResponsibleID>
            <SLAID/>
            <ServiceID/>
            <State>closed unsuccessful</State>
            <StateID>3</StateID>
            <StateType>closed</StateType>
            <TicketID>32</TicketID>
            <TicketNumber>515422152827</TicketNumber>
            <Title>Foofoo my title</Title>
            <Type>Divers</Type>
            <TypeID>1</TypeID>
            <UnlockTimeout>1400239459</UnlockTimeout>
            <UntilTime>0</UntilTime>
         </Ticket>
"""

SAMPLE_TICKET_W_ARTICLES = """<Ticket>
        <Age>863982</Age>
        <ArchiveFlag>n</ArchiveFlag>
        <Article>
                  <Age>863982</Age>
          <AgeTimeUnix>863982</AgeTimeUnix>
          <ArticleID>101</ArticleID>
          <ArticleType>email-external</ArticleType>
          <ArticleTypeID>1</ArticleTypeID>
          <Body>
Bonjour,

Voir echange ci-dessous.

Cdlt.

          </Body>
          <Cc>ACME-CORP - John DOE &lt;john.doe@exemple.fr&gt;</Cc>
          <CcRealname>ACME-CORP - John DOE</CcRealname>
          <Changed>2014-05-16 11:24:19</Changed>
          <Charset>utf-8</Charset>
          <ContentCharset>utf-8</ContentCharset>
          <ContentType>text/plain; charset=utf-8</ContentType>
          <CreateTimeUnix>1400234702</CreateTimeUnix>
          <Created>2014-05-16 10:05:02</Created>
          <CreatedBy>1</CreatedBy>
          <CustomerID>1001</CustomerID>
          <CustomerUserID>user1</CustomerUserID>
          <EscalationResponseTime>0</EscalationResponseTime>
          <EscalationSolutionTime>0</EscalationSolutionTime>
          <EscalationTime>0</EscalationTime>
          <EscalationUpdateTime>0</EscalationUpdateTime>
          <From>John DOE &lt;john.doe@exemple.fr&gt;</From>
          <FromRealname>John DOE</FromRealname>
          <InReplyTo>&lt;1586719931.242426547.1400234690351.JavaMail.zimbra@exemple.fr&gt;</InReplyTo>
          <IncomingTime>1400234702</IncomingTime>
          <Lock>unlock</Lock>
          <LockID>1</LockID>
          <MessageID>&lt;1586719931.242426547.1400234690351.JavaMail.zimbra@exemple.fr&gt;</MessageID>
          <MimeType>text/plain</MimeType>
          <Owner>admin</Owner>
          <OwnerID>2</OwnerID>
          <Priority>3 normal</Priority>
          <PriorityID>3</PriorityID>
          <Queue>Support</Queue>
          <QueueID>2</QueueID>
          <RealTillTimeNotUsed>0</RealTillTimeNotUsed>
          <References />
          <ReplyTo />
          <Responsible>admin</Responsible>
          <ResponsibleID>1</ResponsibleID>
          <SLA />
          <SLAID />
          <SenderType>customer</SenderType>
          <SenderTypeID>3</SenderTypeID>
          <Service />
          <ServiceID />
          <State>closed unsuccessful</State>
          <StateID>3</StateID>
          <StateType>closed</StateType>
          <Subject>Title</Subject>
          <TicketID>32</TicketID>
          <TicketNumber>515422152827</TicketNumber>
          <Title>TEST msg</Title>
          <To>support test  &lt;support-test@exemple.fr&gt; </To>
          <ToRealname>Support test</ToRealname>
          <Type>Divers</Type>
          <TypeID>1</TypeID>
          <UntilTime>0</UntilTime>
        </Article>
        <ChangeBy>2</ChangeBy>
        <Changed>2014-05-16 11:24:19</Changed>
        <CreateBy>1</CreateBy>
        <CreateTimeUnix>1400234702</CreateTimeUnix>
        <Created>2014-05-16 10:05:02
        </Created>
        <CustomerID>1001
        </CustomerID>
        <CustomerUserID>user1</CustomerUserID>
        <EscalationResponseTime>0</EscalationResponseTime>
        <EscalationSolutionTime>0</EscalationSolutionTime>
        <EscalationTime>0</EscalationTime>
        <EscalationUpdateTime>0</EscalationUpdateTime>
        <GroupID>1</GroupID>
        <Lock>unlock</Lock>
        <LockID>1</LockID>
        <Owner>admin</Owner>
        <OwnerID>2</OwnerID>
        <Priority>3 normald</Priority>
        <PriorityID>3</PriorityID>
        <Queue>Support</Queue>
        <QueueID>2</QueueID>
        <RealTillTimeNotUsed>0</RealTillTimeNotUsed>
        <Responsible>admin</Responsible>
        <ResponsibleID>1</ResponsibleID>
        <SLAID />
                <ServiceID />
        <State>closed unsuccessful</State>
        <StateID>3</StateID>
        <StateType>closed</StateType>
        <TicketID>32</TicketID>
        <TicketNumber>515422152827</TicketNumber>
        <Title>Test ticket</Title>
        <Type>Divers</Type>
        <TypeID>1</TypeID>
        <UnlockTimeout>1400239459</UnlockTimeout>
        <UntilTime>0</UntilTime>
      </Ticket>"""

if not MISSING_VARS:

    class TestOTRSAPI(unittest.TestCase):
        def setUp(self):
            self.c = GenericInterfaceClient(OTRS_SERVER, tc=GenericTicketConnectorSOAP(OTRS_WEBSERVICE))
            self.c.register_credentials(OTRS_LOGIN, OTRS_PASSWORD)

        def test_session_create(self):
            sessid = self.c.tc.SessionCreate(user_login=OTRS_LOGIN,
                                             password=OTRS_PASSWORD)
            self.assertEqual(len(sessid), 32)

        def test_ticket_get(self):
            t = self.c.tc.TicketGet(1)
            self.assertEqual(t.TicketID, 1)
            self.assertEqual(t.StateType, 'new')

        def test_ticket_get_with_articles(self):
            t = self.c.tc.TicketGet(1, get_articles=True)
            self.assertEqual(t.TicketID, 1)
            self.assertEqual(t.StateType, 'new')
            articles = t.articles()
            self.assertIsInstance(articles, (list, tuple))
            self.assertIsInstance(articles[0], Article)
            self.assertEqual(articles[0].SenderType, 'customer')

        def test_ticket_search(self):
            t_list = self.c.tc.TicketSearch(Title='Welcome to OTRS!')
            self.assertIsInstance(t_list, list)
            self.assertIn(1, t_list)

        def test_ticket_create(self):
            t = Ticket(State='new',
                       Priority='3 normal',
                       Queue='Postmaster',
                       Title='Problem test',
                       CustomerUser='user1',
                       Type='Unclassified')
            a = Article(Subject='UnitTest',
                        Body='bla',
                        Charset='UTF8',
                        MimeType='text/plain')
            t_id, t_number = self.c.tc.TicketCreate(t, a)
            self.assertIsInstance(t_id, int)
            self.assertIsInstance(t_number, int)
            self.assertTrue(len(str(t_number)) >= 12)
            exit

        def test_ticket_update_attrs_by_id(self):
            t = Ticket(State='new',
                       Priority='3 normal',
                       Queue='Postmaster',
                       Title='Problem test',
                       CustomerUser='user1',
                       Type='Unclassified')
            a = Article(Subject='UnitTest',
                        Body='bla',
                        Charset='UTF8',
                        MimeType='text/plain')
            t_id, t_number = self.c.tc.TicketCreate(t, a)

            t = Ticket(Title='Foubar')
            upd_tid, upd_tnumber = self.c.tc.TicketUpdate(ticket_id=t_id,
                                                          ticket=t)
            self.assertIsInstance(upd_tid, int)
            self.assertIsInstance(upd_tnumber, int)
            self.assertTrue(len(str(upd_tnumber)) >= 12)

            self.assertEqual(upd_tid, t_id)
            self.assertEqual(upd_tnumber, t_number)

            upd_t = self.c.tc.TicketGet(t_id)
            self.assertEqual(upd_t.Title, 'Foubar')
            self.assertEqual(upd_t.Queue, 'Postmaster')

        def test_ticket_update_attrs_by_number(self):
            t = Ticket(State='new',
                       Priority='3 normal',
                       Queue='Postmaster',
                       Title='Problem test',
                       CustomerUser='user1',
                       Type='Unclassified')
            a = Article(Subject='UnitTest',
                        Body='bla',
                        Charset='UTF8',
                        MimeType='text/plain')
            t_id, t_number = self.c.tc.TicketCreate(t, a)

            t = Ticket(Title='Foubar')
            upd_tid, upd_tnumber = self.c.tc.TicketUpdate(ticket_number=t_number,
                                                          ticket=t)
            self.assertIsInstance(upd_tid, int)
            self.assertIsInstance(upd_tnumber, int)
            self.assertTrue(len(str(upd_tnumber)) >= 12)

            self.assertEqual(upd_tid, t_id)
            self.assertEqual(upd_tnumber, t_number)

            upd_t = self.c.tc.TicketGet(t_id)
            self.assertEqual(upd_t.Title, 'Foubar')
            self.assertEqual(upd_t.Queue, 'Postmaster')

        def test_ticket_update_new_article(self):
            t = Ticket(State='new',
                       Priority='3 normal',
                       Queue='Postmaster',
                       Title='Problem test',
                       CustomerUser='user1',
                       Type='Unclassified')
            a = Article(Subject='UnitTest',
                        Body='bla',
                        Charset='UTF8',
                        MimeType='text/plain')
            t_id, t_number = self.c.tc.TicketCreate(t, a)

            a2 = Article(Subject='UnitTest2',
                         Body='bla',
                         Charset='UTF8',
                         MimeType='text/plain')

            a3 = Article(Subject='UnitTest3',
                         Body='bla',
                         Charset='UTF8',
                         MimeType='text/plain')

            self.c.tc.TicketUpdate(t_id, article=a2)
            self.c.tc.TicketUpdate(t_id, article=a3)

            t_upd = self.c.tc.TicketGet(t_id, get_articles=True)
            arts_upd = t_upd.articles()
            self.assertIsInstance(arts_upd, list)
            self.assertEqual(len(arts_upd), 3)
            self.assertEqual(arts_upd[0].Subject, 'UnitTest')
            self.assertEqual(arts_upd[1].Subject, 'UnitTest2')
            self.assertEqual(arts_upd[2].Subject, 'UnitTest3')

else:
    print("Set OTRS_LOGIN, OTRS_PASSWORD, OTRS_SERVER and OTRS_WEBSERVICE\n"
        "env vars if you want to run tests against a REAL OTRS web service\n\n"
        "example:\n\n"
        "export OTRS_LOGIN=mylogin\n"
        "export OTRS_PASSWORD=mypassword\n"
        "export OTRS_SERVER=https://myotrs.example.com\n"
        "export OTRS_WEBSERVICE=GenericTicketConnectorSOAP\n")


class TestObjects(unittest.TestCase):
    def test_ticket(self):
        t = Ticket(TicketID=42, EscalationResponseTime='43')
        self.assertEqual(t.TicketID, 42)
        self.assertEqual(t.EscalationResponseTime, 43)

    def test_ticket_from_xml(self):
        xml = etree.fromstring(SAMPLE_TICKET)
        t = Ticket.from_xml(xml)
        self.assertEqual(t.TicketID, 32)
        self.assertEqual(t.CustomerUserID, 'user1')

    def test_ticket_from_xml_with_articles(self):
        xml = etree.fromstring(SAMPLE_TICKET_W_ARTICLES)
        t = Ticket.from_xml(xml)
        self.assertEqual(t.TicketID, 32)
        self.assertEqual(t.CustomerUserID, 'user1')
        articles = t.articles()
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 1)
        self.assertIsInstance(articles[0], Article)
        self.assertEqual(articles[0].AgeTimeUnix, 863982)

    def test_ticket_to_xml(self):
        t = Ticket(State='open', Priority='3 normal', Queue='Postmaster')
        xml = t.to_xml()
        xml_childs = xml.getchildren()

        xml_childs_dict = {i.tag: i.text for i in xml_childs}

        self.assertEqual(xml.tag, 'Ticket')
        self.assertEqual(len(xml_childs), 3)
        self.assertEqual(xml_childs_dict['State'], 'open')
        self.assertEqual(xml_childs_dict['Priority'], '3 normal')
        self.assertEqual(xml_childs_dict['Queue'], 'Postmaster')


if __name__ == '__main__':
    unittest.main()
