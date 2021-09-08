import http.client
import json
import csv
from copy import deepcopy

GT_USERNAME = 'dhislop3'
TMDB_API_KEY = 'redacted'
TMDB_URL = 'api.themoviedb.org'
TMDB_VERSION = '3'
TMDB_LANG = 'en-US'



#############################################################################################################################
# cse6242 
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
#
#############################################################################################################################


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def node_exists(self, node):
        """ check to see if a node exists already """
        return (node in self.nodes)

    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        assert isinstance(id, str)
        assert isinstance(name, str)
        name = name.replace(',', '')
        if not self.node_exists((id, name)):
            self.nodes.append((id, name))

    def edge_exists(self, a, b):
        """ Return true if an edge exists already, in either order """
        return ((a,b) in self.edges or (b,a) in self.edges or b == a)

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        assert isinstance(source, str)
        assert isinstance(target, str)

        if not self.edge_exists(source, target):
            self.edges.append((source, target))

    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)


    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)

    def find_non_leaf_node_count(self) -> dict:
        """ given a dict of counts for all node_ids, return a count of nodes only appearing once """
        leaf_nodes = {}
        ids_with_lowest_degree = [id for id, count in self.dn.items() if count == 1] # find ids appearing once
        for id in ids_with_lowest_degree:
            leaf_nodes[id] = self.dn[id]
        non_leaf_count = len(self.dn) - len(leaf_nodes)
        print("total number of nodes", len(self.dn))
        print("total number of leaf nodes:", len(leaf_nodes))
        print("total number of non-leaf nodes:", non_leaf_count )

        return non_leaf_count

    def find_lowest_degree(self) -> dict:
        """ given a dict of counts for all node_ids, find the ones that appear the least. return multiple if tied """
        output = {}
        highest_degree = min(self.dn.values()) # find lowest count value
        ids_with_highest_degree = [id for id, count in self.dn.items() if count == highest_degree] # find ids with highest count value
        for id in ids_with_highest_degree:
            output[id] = self.dn[id]
        
        return output

    def find_highest_degree(self, count_dict) -> dict:
        """ given a dict of counts for all node_ids, find the one that appears the most. return multiple if tied """
        output = {}
        highest_degree = max(count_dict.values()) # find highest count value
        ids_with_highest_degree = [id for id, count in count_dict.items() if count == highest_degree] # find ids with highest count value
        for id in ids_with_highest_degree:
            output[id] = count_dict[id]
        
        return output

    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree # e.g. how many times the id appears in the edges
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        list_of_ids = []
        for x, y in self.edges:     # may not be efficient, but put all source and target ids into one long list
            list_of_ids.append(x)
            list_of_ids.append(y)

        self.dn = dict((x,list_of_ids.count(x)) for x in set(list_of_ids))   # count occurences of each id in list
        mdn = self.find_highest_degree(self.dn)
        return mdn

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key = api_key

    def form_url_person_detail(self, search_id):
        self.url = '/' + TMDB_VERSION + '/person/' + search_id + '?api_key=' + TMDB_API_KEY + '&language=' + TMDB_LANG

    def form_url_person_credits(self, search_id):
        self.url = '/' + TMDB_VERSION + '/person/' + search_id + '/movie_credits' + '?api_key=' + TMDB_API_KEY + '&language=' + TMDB_LANG

    def form_url_movie_credits(self, search_id):
        self.url = '/' + TMDB_VERSION + '/movie/' + search_id + '/credits' + '?api_key=' + TMDB_API_KEY + '&language=' + TMDB_LANG

    def form_url_search(self, search_id):
        self.url = '/' + TMDB_VERSION + '/search/person' + '?api_key=' + TMDB_API_KEY + '&language=' + TMDB_LANG + '&query=' + search_id 

    def lookup(self):
        conn = http.client.HTTPSConnection(TMDB_URL)

        #print("looking up ", self.url)
        conn.request("GET", self.url)

        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        if r1.status == 200:
            string_data1 = r1.read().decode('utf-8')
            data1 = json.loads(string_data1)
        return data1

    def get_filtered_movie_cast(self, api_response:dict, limit:int=None, exclude_ids:list=None)->list:
        """ note I am not ordering the results, only using the 'order' field returned to limit"""
        #print("\n", api_response, "\n")
        output = []
        if limit == None: #  if no limit is specified, set to arbitrarily high int so that it can be compared, unlike None
            filtered_limit=99999
        else:
            filtered_limit=limit-1

        if exclude_ids == None:
            filtered_exclude_ids = []
        else:
            filtered_exclude_ids = exclude_ids

        if 'cast' in api_response:
            for item in api_response['cast']:
                if item['id'] in filtered_exclude_ids:
                    pass
                elif item['order'] <= filtered_limit:
                    output.append({'id':item['id'], 'character':item['character'], 'name':item['name'], 'credit_id':item['credit_id']})
                    #temp
                    #print({'id':item['id'], 'character':item['character'], 'credit_id':item['credit_id'], 'name':item['name'], 'order':item['order']})
        return output

    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param integer movie_id: a movie_id
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.

        Important: the exclude_ids processing should occur prior to limiting output.
        """
        print("processing movie id", movie_id)
        self.form_url_movie_credits(str(movie_id)) #should this be a string?
        response = self.lookup()
        filtered_response = self.get_filtered_movie_cast(response, limit, exclude_ids)

        return filtered_response

    # This function may not be needed - or its replicated in main
    def get_cast_from_movie_ids(self, credits:list, limit=None, exclude_ids:list=None):
        """ loop through each movie id in credits, getting the cast for each movie """
        for item in credits:
            self.get_movie_cast(item['id'], limit, exclude_ids)

    def get_filtered_movie_credits(self, api_response:dict, vote_avg_threshold:float=None)->list:
        output = []
        if vote_avg_threshold == None:
            filtered_vote_avg_threshold=0.0 # if no threshold, set to arbitrarily low
        else:
            filtered_vote_avg_threshold=vote_avg_threshold

        if 'cast' in api_response:
            for item in api_response['cast']:
                if item['vote_average'] >= filtered_vote_avg_threshold:
                    output.append({'id':item['id'], 'title':item['title'], 'vote_avg':item['vote_average']})
        return output

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        self.form_url_person_credits(person_id)
        response = self.lookup()
        filtered_response = self.get_filtered_movie_credits(response, vote_avg_threshold)

        return filtered_response

def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return GT_USERNAME

def return_argo_lite_snapshot()->str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    return 'https://poloclub.github.io/argo-graph-lite/#749377dc-0daf-4958-afc8-2eb6d375b4b2'



# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

if __name__ == "__main__":
    # tmdb_api_utils.form_url_person_detail('2975')
    # response = tmdb_api_utils.lookup()
    # credits = tmdb_api_utils.get_movie_credits_for_person('1397778') # Anya    
    # print(credits)
    # print(graph.max_degree_nodes())

    # INITIALIZE SUMMARY GRAPH
    graph_summary = Graph()

    # BEGIN BUILD CO-ACTOR NETWORK
    #
    # INITIALIZE GRAPH
    print(return_name())
    graph = Graph()
    tmdb_api_utils = TMDBAPIUtils(api_key=TMDB_API_KEY)
    #   Initialize a Graph object with a single node representing Laurence Fishburne
    graph.add_node(id='2975', name='Laurence Fishburne')
    graph.print_nodes()



    # BEGIN BUILD BASE GRAPH:
    #   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
    # graph_base = Graph()
    # base_credits = tmdb_api_utils.get_movie_credits_for_person('2975', 8.0)
    # print("credits meeting 8.0 for LF ", base_credits)
    #   FOR each movie credit:
    # for movie in base_credits:
    # #   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
    #     cast = tmdb_api_utils.get_movie_cast(movie['id'], 1, ['2975'])   # set to 3

    # #   |   FOR each movie cast member:
    #     for member in cast:
    #         graph_base.add_node(str(member['id']), member['name'])
    #         graph_base.add_edge(source='2975', target=str(member['id']))
    #   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
    #   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
    #   |   |   and each new node (co-actor/co-actress)
    #   |   END FOR
    #   END FOR
    # END BUILD BASE GRAPH

    #
    #
    # BEGIN LOOP - DO 2 TIMES:
    #   IF first iteration of loop:
    #   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
    #   ELSE
    #   |    nodes = The nodes added in the previous iteration:
    #   ENDIF

    for loop in range(3):
        if loop == 0:
            print(f"*** START LOOP {loop} ********************************************************************************************************************{loop}")
            # Loop 0 is formerly base loop
            nodes = deepcopy(graph.nodes) # This must be BEFORE resetting graph)now below
            graph_base = Graph()
            graph_now = deepcopy(graph_base)
            print("instantiating graph_now, it has", graph_now.print_nodes())

        elif loop == 1:
            print(f"*** START LOOP {loop} ********************************************************************************************************************{loop}")
            nodes = deepcopy(graph_now.nodes) # This must be BEFORE resetting graph)now below
            graph_loop1 = Graph()
            graph_now = deepcopy(graph_loop1)
            print("instantiating graph_now, it has", graph_now.print_nodes())

        elif loop == 2:
            print(f"*** START LOOP {loop} ********************************************************************************************************************{loop}")
            nodes = deepcopy(graph_now.nodes) # This must be BEFORE resetting graph)now below
            graph_loop2 = Graph()
            graph_now = deepcopy(graph_loop2)
            print("instantiating graph_now, it has", graph_now.print_nodes())

        else:
            pass

        for node in nodes:
            print("my node is", node)
            node_credits = tmdb_api_utils.get_movie_credits_for_person(node[0], 8.0)
            print(f"credits meeting 8.0 for {node[1]}")
            #   FOR each movie credit:
            for movie in node_credits:
            #   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
                cast = tmdb_api_utils.get_movie_cast(movie['id'], 1, [node[0]])  # set to 3

            #   |   FOR each movie cast member:
                for member in cast:
                    graph_now.add_node(str(member['id']), member['name'])
                    graph_now.add_edge(source=str(node[0]), target=str(member['id']))
            #   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
            #   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
            #   |   |   and each new node (co-actor/co-actress)
            #   |   END FOR
            #   END FOR
            # END BUILD BASE GRAPH
        
        # Now add this current loop to the summary graph:
        for node in graph_now.nodes:
            graph_summary.add_node(node[0], node[1])
        for edge in graph_now.edges:
            graph_summary.add_edge(edge[0], edge[1])
        
        print(f"-{len(graph_now.nodes)}-nodes loop {loop}---")
        graph_now.print_nodes()
        print(f"-{len(graph_now.edges)}--edges loop {loop}---")
        graph_now.print_edges()

    print(f"-{len(graph_base.nodes)}-base nodes---")
    graph_base.print_nodes()
    print(f"-{len(graph_base.edges)}--base edges---")
    graph_base.print_edges()

    print(f"-{len(graph.nodes)}--original nodes---")
    graph.print_nodes()
        
    print(f"-{len(graph_summary.nodes)}--SUMMARY nodes---")
    graph_summary.print_nodes()
    print(f"-{len(graph_summary.edges)}--SUMMARY edges---")
    graph_summary.print_edges()


    # graph_summary.write_edges_file()
    # graph_summary.write_nodes_file()

    #   FOR each node in nodes:
    #   |  get the movie credits for the actor that have a vote average >= 8.0
    #   |
    #   |   FOR each movie credit:
    #   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
    #   |   |
    #   |   |   FOR each movie cast member:
    #   |   |   |   IF the node doesn't already exist:
    #   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
    #   |   |   |   ENDIF
    #   |   |   |
    #   |   |   |   IF the edge does not exist:
    #   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
    #   |   |   |   ENDIF
    #   |   |   END FOR
    #   |   END FOR
    #   END FOR
    # END LOOP
    #
    # Your graph should not have any duplicate edges or nodes
    # Write out your finished graph as a nodes file and an edges file using:
    #   graph.write_edges_file()
    #   graph.write_nodes_file()
    #
    # END BUILD CO-ACTOR NETWORK
    # ----------------------------------------------------------------------------------------------------------------------

    # Exception handling and best practices
    # - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
    # - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
    # - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
    # - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
    #   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
    #   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.


    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    # graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")


    #############################################################################################################################
    #
    # BUILDING YOUR GRAPH
    #
    # Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
    #
    # Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
    # In this graph, each node represents an actor
    # An edge between any two nodes indicates that the two actors/actresses acted in a movie together
    # i.e., they share a movie credit.
    # e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
    # or more movies together.
    #
    # For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
    # we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
    # Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
    #
    # You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
    # algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
    # snapshot.
    #
    # GRAPH SIZE
    # With each iteration of your graph build, the number of nodes and edges grows approximately at an exponential rate.
    # Our testing indicates growth approximately equal to e^2x.
    # Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
    # you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
    # updating the auto-grader.  We establish a bound for lowest & highest encountered numbers of nodes and edges with a
    # margin of +/- 100 for nodes and +/- 150 for edges.  e.g., The allowable range of nodes is set to:
    #
    # Min allowable nodes = min encountered nodes - 100
    # Max allowable nodes = max allowable nodes + 100
    #
    # e.g., if the minimum encountered nodes = 507 and the max encountered nodes = 526, then the min/max range is 407-626
    # The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
    # ----------------------------------------------------------------------------------------------------------------------
