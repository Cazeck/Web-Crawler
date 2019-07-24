from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import matplotlib.pyplot as plt
import networkx as nx
import csv
 
#Casey Kolodziejczyk

class LinkParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]
                    
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        self.feed(htmlString)
        return htmlString, self.links



visitedPages = []   #Each page the crawler goes through.
numberNodes = []    #For each visited page.
edges = []          #For each visited page. *It is a list of lists*
d = []
externalLinks = []

domain = 'cs.uiowa.edu'


G = nx.Graph()
G2 = nx.Graph()

def spider(url):
    pagesToVisit = [url] 
    while pagesToVisit != [] and len(visitedPages) < 100:

        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        #print("toVisit:", len(pagesToVisit))
        
        try:
            
            if(url.find(domain) != -1): #url is valid
            
                parser = LinkParser()
                data, links = parser.getLinks(url)
                
                #add to list of edges: source, target
                for k in links:
                    d.append([url,k])

                    # Added in After 
                    if(k.find(domain) != -1):  # If the link is still within the domain

                        edges.append([url, k])
                    
                #add visited page
                visitedPages.append(url)
                
                #remove links to previously visited pages before adding to pages to Visit
                newLinks = [x for x in links if x not in visitedPages]
                
                #Make sure we are not adding duplicates to pagesToVisit
                newLinks = [x for x in newLinks if x not in pagesToVisit]                
                
                #add any new pages to visit 
                pagesToVisit = pagesToVisit + newLinks
               
                #increase number of nodes by number new links found
                numberNodes.append(len(links))
                #visited page
                #print("new links:", len(newLinks))
                
            else:
                visitedPages.append(url)
                #externalLinks.append(url)
            
        except:
            print(" **Failed to parse!**")

#decode to write to csv in utf-8 
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

#Begin Crawl        
spider("http://cs.uiowa.edu/")

#Write to CSV

#with open("memeOutput.csv", "w", encoding='utf-8') as f:
 #   writer = csv.writer(f,lineterminator = '\n' )
  #  writer.writerow(['source', 'target'])
   # utf_8_encoder(writer.writerows(d))



G2.add_nodes_from(visitedPages)
G2.add_edges_from(edges)


print(len(visitedPages))

print(visitedPages)

print("noNodes")

print(numberNodes)

print("edges")

print(edges)

print("d")

print()


nx.draw(G2, node_size= 5, with_labels=False)
plt.show()






