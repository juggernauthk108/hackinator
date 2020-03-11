import requests
from lxml import html
import xlsxwriter

wb=xlsxwriter.Workbook('output.xlsx')
ws=wb.add_worksheet()

#GET THE LIST OF THE SERVICES
awsPage=requests.get("https://www.cloudconformity.com/knowledge-base/aws/")
awsTree=html.fromstring(awsPage.content)
awsList=awsTree.xpath('//ul[@class="service-list"]/li[@class="service-link"]/h2/a/text()')
#print awsList
#print len(awsList)

row=0
brow=0
for x in range(len(awsList)):
    print awsList[x]
    serviceList=awsTree.xpath('(//li[@class="service-link"])['+str(x+1)+']//ul/li[@class="rule-link"]//p/text()')
    #print serviceList
    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    #get the number of links for every baseline
    #iterate over each link and get the steps

    BS_steps=awsTree.xpath('(//li[@class="service-link"])['+str(x+1)+']//ul/li[@class="rule-link"]//a/@href')
    
    
    for baseline in serviceList:
        ws.write(row,0,awsList[x])
        ws.write(row,1,baseline)
        row += 1
    serviceList=[]
    
    for steps in range(len(BS_steps)):
	stepPage=requests.get('https://www.cloudconformity.com'+BS_steps[steps])
        print BS_steps[steps]
        stepTree=html.fromstring(stepPage.content)
        stepList=stepTree.xpath('(//div[@class="overlay"])[2]//p//text()')
	stepList2=stepTree.xpath('(//div[@class="overlay"])[4]//p//text()')
	riskLevel=stepTree.xpath('(//div[@class="risk-level"]//text())[3]')
        ws.write(brow,3," ".join(riskLevel))
        ws.write(brow,4," ".join(stepList))
	ws.write(brow,5," ".join(stepList2))
        brow +=1
		
wb.close()
#print serviceList



#Getting the baseline links
indexPage=requests.get('https://www.cloudconformity.com/knowledge-base/aws/')
indexTree=html.fromstring(indexPage.content)
print indexTree.xpath('//ul[@class="service-list"]/li[@class="service-link"]/h2/a/@href') #relative links of all services

#PSEUDO CODE TO  GET THE CONSOLE STEPS
pageContent=requests.get("https://www.cloudconformity.com/knowledge-base/aws/ACM/expired-certificate.html")
tree=html.fromstring(pageContent.content)
step1=tree.xpath('(//div[@class="overlay"])[2]//p/text()')

#cleaning steps
step2=[x.replace("\n","") for x in step1]
step3=[x.replace("\t","") for x in step2]

#remove empty elemets
#print [i for i in step3 if i] 


#PSEUDO CODE TO GET CLI STEPS
cliSteps=requests.get("https://www.cloudconformity.com/knowledge-base/aws/ACM/expired-certificate.html")
cli_tree=html.fromstring(cliSteps.content)
cli_step=cli_tree.xpath('(//div[@class="overlay"])[4]//p/text()')
#print cli_step
