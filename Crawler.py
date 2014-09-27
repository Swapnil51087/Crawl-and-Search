
''' Function to rank pages. The input parameter is a graph(dictionary) 
which contains url as key and list of urls which are found on the url as value '''
def rank(graph): 
     d = 0.8 # damping factor 
     numloops = 10
    
     ranks = {} #dictionary which contains ranks of pages 
     npages = len(graph) 
     for page in graph: #for every page in graph compute its rank
        ranks[page] = 1.0 / npages #Initialized to 1.0 / npages in graph.. it is the initial probability
        
     for i in range(0, numloops): # Step function to calculate rank. More the step factor more is accuracy
        newranks = {}
        
        for page in graph: #browse through every page in graph and assign a new value to it
            newrank = (1 - d) / npages
            
            for node in graph: # Check wherever the current page exists in graph and calculate its newrank
                if page in graph[node]:
                    newrank = newrank + d * (rank[page]/len(graph[node]))
            
            newranks[page] = newrank
        
        ranks = newranks
        
     return ranks
    
#get the content of the web page from url
def get_content(url): 
    try:
		import urllib
		return urllib.urlopen(url).read()
		
    except:
       return ""

# get the next link on the page   
def get_next_link(page): 
    target = "a href=" # target string to look for in the page
    start_index = page.find(target) #First index where target is found
    if start_index == -1: # if target not found return None else return url and its end_index
        return None, 0
    start_quote = page.find('"', start_index)
    end_quote = page.find('"', start_quote + 1)
    link = page[start_quote + 1: end_quote]
    
    return link, end_quote
    
#to retrieve the list of urls exists on a web page
def get_list_of_urls(page): 
    links = []
    while True: # get links till the end of  the page.. break if no more links exists
        url, end_quote = get_next_link(page) 
        if url:
            links.append(url)
            page = page[end_quote:]
            
        else:
            break
    
    return links

#adds list of urls to to be crawled pages list    
def union(to_crawl, urls): 
    for entry in urls:
                if entry not in to_crawl:
                    to_crawl.append(entry)
                    
# initiates crawling with seed page   
def crawl(seed): 
    index = {}
    to_crawl = [seed]
    crawled = []
    graph = {}
    count = 0
    while to_crawl and count < 3:
        url = to_crawl.pop()
        if url not in crawled: # Check whether url has been crawled or not
            content = get_content(url) 
            add_page_to_index(index, url, content) #add the current page to the index
            url_list = get_list_of_urls(content) # get the list of urls for this page
            graph[url] = url_list
            union(to_crawl, url_list)
            crawled.append(url)
            
        count = count + 1
        
    return index
# add a url to its associated keyword
def add_to_index(index, keyword, url):
    for entry in index: 
        if entry == keyword:
            if url not in index[entry]:
                index[entry].append(url)
                return
                
    index[keyword] = [url]                

#add pages to index
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
# a look function to find whether a keyword exists in the index or not
def lookup(index, keyword):
    for entry in index:
        if entry == keyword:
            return index[entry]
    return None
        
    
        
        
        
        
            
