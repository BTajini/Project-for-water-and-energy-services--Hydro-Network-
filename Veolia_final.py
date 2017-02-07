#-*- encoding: utf-8 -*-

#---Author--- : Badr Tajini
#---Contributor--- : Michael Faivre
#---Campus--- : Paris (On-Campus)
#---Release--- : 16/10/2016 - V5.0
#---Project : VEOLIA HYDRONETWORK

#library implemented in the project
from collections import defaultdict
import sys
import os
from time import time
import psutil # must be installed first or deleted (library for calculating memory allocated in every current implementation)

#calculate memory allocated for every implementation  !!!!need install library psutil-4.3.1 or delete line below with import psutil!!!!
process = psutil.Process(os.getpid())#delete this line if you can't donwload and install library psutil-4.3.1
print('Memory allocated for this implementation :',(process.memory_info().rss),'\n')
'----------------------------------------------------'
#define local variable for running time of algorithm
ta = time()
print('starting time',ta)
#sys.exit()
'----------------------------------------------------'


#list_nodes : list of source,destination nodes
list_nodes=[]

##read PIPES
Flag_Pipes = False
list_pipes = []
##read VALVES
Flag_Valves = False
list_valves = []

#stackoverfow:python - Read file from and to specific lines of text
with open('C:\Users\Badr\PycharmProjects\Project_Metro_Paris\water_network.txt', "r") as filename:
	for i, line in enumerate(filename.readlines()):
		if 'PIPES' in line:
			Flag_Pipes = True
			print ("Started at line in PIPES", i)
			continue
		if 'PUMPS' in line:
			print ("End at line", i)
			Flag_Pipes = False
			#break
		if 'VALVES' in line:
			Flag_Valves = True
			print ("Started at line in VALVES", i)
			continue
		if 'TAGS' in line:
			print ("end at line", i)
			Flag_Valves = False
			break
                # Process for Pipeline
		if Flag_Pipes == True:
		        
                        new_list = line.split()[0:3] #[0]=EdgeID, [1]=N1, [2]=N2
                        new_list.append('0')       
                        new_list.append('open')
                        list_pipes.append(new_list)
		if Flag_Valves == True:
                        new_list = line.split()[0:3] #[0]=EdgeID, [1]=N1, [2]=N2
                        new_list.append('1')
                        new_list.append('open')
                        list_valves.append(new_list) 

filename.close()
list_pipes=list_pipes[1:-1]
print("list_pipes")
print(list_pipes[0:20]) #
print(type(list_pipes))


list_valves=list_valves[1:-1]
print("list_valves")
print(list_valves[0:20]) #
print(type(list_valves))
#sys.exit()
#implementation of 2 lists : 1 for PIPES & 1 for VALVES


#ADD EDGE_ID IN THE STRUCTURE and add dictionary fro graph processing
dict_for_pipes = {}
for item in list_pipes:
    key = "/".join(item[:-4])  #-1])
    dict_for_pipes.setdefault(key, []).append(item[1])  #Node1
    dict_for_pipes.setdefault(key, []).append(item[2])  #Node2
    dict_for_pipes.setdefault(key, []).append(item[0])  #EdgeID
    dict_for_pipes.setdefault(key, []).append(item[3])  #Flag
    dict_for_pipes.setdefault(key, []).append(item[4])  #Status


##### local variable for test printing of PIPES dictionary
dict_pairs = {k: dict_for_pipes[k] for k in sorted(dict_for_pipes.keys())[:3]}
#print(dict_pairs)

#ADD EDGE_ID IN THE STRUCTURE and add dictionary fro graph processing
dict_for_valves = {}
for item in list_valves:
    key = "/".join(item[:-4])  #-1])
    dict_for_valves.setdefault(key, []).append(item[1])  #Node1
    dict_for_valves.setdefault(key, []).append(item[2])  #Node2
    dict_for_valves.setdefault(key, []).append(item[0])  #Edge
    dict_for_valves.setdefault(key, []).append(item[3])  #Flag
    dict_for_valves.setdefault(key, []).append(item[4])  #Status
# TEST print VALVES dictionary 

#MERGE 2 dictionaries
dict_merge = dict(dict_for_pipes)
dict_merge.update(dict_for_valves)
# local variable for test printing of VALVES dictionary 
dict_pairs = {k : dict_merge[k] for k in sorted(dict_merge.keys())[:3]}
print(dict_pairs)


#INVERSE MAPPING USING A CONCATENATION OF NODES
def concat_Nodes(Na,Nb):
        return 'N1-'+Na+'-N2-'+Nb

Inv_dict_Temp = defaultdict(list)
for k,v in dict_merge.items():
        Nodes_Edge = concat_Nodes(v[0],v[1])
        Inv_dict_Temp[Nodes_Edge].append(k)
Inv_dict_merge = dict(Inv_dict_Temp)
print(Inv_dict_merge)
##sys.exit() 

#DICT OF NODES adjacencies

temp_dict_Nodes = defaultdict(list)
for k,v in dict_merge.items():
        temp_dict_Nodes[v[0]].append(v[1:])
        ## SWAP 
        if v[2] != '0' and v[2] !='1': 
                temp_dict_Nodes[v[1]].append(list((v[0],v[2],v[3],v[4])))  

dict_Nodes_Edges_W_Flags = dict(temp_dict_Nodes)
print(dict_Nodes_Edges_W_Flags)
print('Neighbours of NV52000403')
print(dict_Nodes_Edges_W_Flags['NV52000403'])
###sys.exit()



#BUILD DICT OF EDGES AND FLAGS FOR ADJACENCY ON EDGES - BFS Version

dict_Edges_W_Flags={}
list_Edge_ID=None
list_Edge_ID=list(dict_merge.keys())
print(list_Edge_ID)
Temp_dict_Edges = defaultdict(list)
#BUILD DICT_EDGES_with_FLAGS
for Current_edge in list_Edge_ID:
        Node1 = dict_merge[Current_edge][0] #to do also with node2
        Node2 = dict_merge[Current_edge][1]
        
        #get Edges connected to Node1 from dict_Node edge flag
        l_curr_Edg_Flg = [] #list of pairs [E,F] 
        for v in dict_Nodes_Edges_W_Flags[Node1]:
                if v[1]!=Current_edge:
                        l_curr_Edg_Flg.append(list((v[1],v[2],v[3])))
        for v in dict_Nodes_Edges_W_Flags[Node2]:
                if v[1]!=Current_edge:
                        l_curr_Edg_Flg.append(list((v[1],v[2],v[3])))
        
        Temp_dict_Edges[Current_edge].append(l_curr_Edg_Flg)
        Temp_dict_Edges[Current_edge] = Temp_dict_Edges[Current_edge][0] # to remove a list
        
        continue
dict_Edges_W_Flags = dict(Temp_dict_Edges)
print('dict_Edges_W_Flags',dict_Edges_W_Flags)



#-----------DfSGRAPH 
#-----------CHANGE STATUS FROM 'OPEN' TO 'CLOSE' FOR VISITED EDGDES 
'---------  Change status of Edge visited ---------'
def Status_Edge_changed_with_dict(graph_Temp,Vertex_EDGE):
    
    for kk,vv in graph_Temp.items():
        
        for mm in range(len(vv)):
                
                if vv[mm][0]==Vertex_EDGE:
                        l_temp_list = graph_Temp[kk]
                        l_temp_list[mm][2] = 'close'
                        graph_Temp[kk] = l_temp_list
    return graph_Temp


'--------- Remove edges from identified Valve Edge -------'
def Remove_Edge_from_dict(graph_Temp,Vertex_EDGE):
    
    try:
        del graph_Temp[Vertex_EDGE]
        for kk,vv in graph_Temp.items():
            if vv[0]==Vertex_EDGE:
                graph_Temp[kk].remove(vv)  #vv=list[Edge,Flag]
                print('Graph_Temp[kk]',graph_Temp[kk])
                print('Vertex_EDGE',Vertex_EDGE)
                sys.exit()
    except:
        return None
    return graph_Temp



#Implementation of DFS FOR EACH INPUT EDGES
def dfs_paths_cycle(graph_search, start):
    '------ Initialize stack, EDGES_TO_CLOSE list, temporary graph ---'
    list_stack = [(start,[start])] #a list of pair(s)
    list_Paths=[]  #list path of a Valve 
    count_a = 0
    sum_count=0
    list_edge_to_close=[]
    visited = set()
    graph_Temp = graph_search
    
    all_Edges_visited = []
   
    '-------------- Loop over stack until the end of the pile !! ------------------'
    while list_stack:
        
        sum_count+=1
        # Gets the last list_path for stack
        
        (Edge,list_path_a) = list_stack.pop()  #dequeue first list_path_a, not just a node!!
        FLAG_cur=Edge[1]
        EDGE_cur=Edge[0]
        STATUS_cur=Edge[2]
        all_Edges_visited.append(Edge)
        Nb_neighbors_count=0


        '---------- Check the status of current EDGE in regards of visited Valve  ------'
        if (EDGE_cur in list_edge_to_close or EDGE_cur in visited or STATUS_cur=='close'):

                continue  #dequeue next path in l_queue

        '---------- Process currrent Edge if it''s written as Valve --------'
        #Test to store list_path_a in list_Paths and Edge in l_VALVE_ID
        if FLAG_cur == '1':
            count_a +=1
            '------ check if path already registered ------'
            if list_path_a not in list_Paths:
                    list_Paths.append(list_path_a)
                    visited.add(EDGE_cur)
                    list_edge_to_close.append(EDGE_cur)
                    #
                    Status_Edge_changed_with_dict(graph_Temp, EDGE_cur) #from 'open' to 'close' on EDGE_cur as adjacent edge
                    Remove_Edge_from_dict(graph_Temp,EDGE_cur)

                    '------- loop for the current valve Edge searching nearest neighbors ---------'

                    for Current_neighbour_new in graph_Temp.get(Prev_EDGE_curr,[]):
                            visited.add(Current_neighbour_new[0])
                            all_Edges_visited.append(Current_neighbour_new)
                            Nb_neighbors_count+=1

                    for ii in range(Nb_neighbors_count-1):
                            #print('Nb_neighbors_count',Nb_neighbors_count)

                            '---------- from previous iteration :  Edge unstacked) --------'
                            (Edge,list_path_a) = list_stack.pop() #get Edges at same graph_level as Edge_curr which neighbors in dfs_paths_cycle
                            FLAG_cur=Edge[1]
                            EDGE_cur=Edge[0]
                            STATUS_cur=Edge[2]

                            Status_Edge_changed_with_dict(graph_Temp, EDGE_cur) #from 'open' to 'close' on EDGE_cur Pipe or Valve
                            Remove_Edge_from_dict(graph_Temp,EDGE_cur)


                            '------------ Update all_Edges_visited -----------'
                            all_Edges_visited.append(Edge)
                            #set all neighbors Valve who it''s detected

                            if (EDGE_cur in list_edge_to_close or EDGE_cur in visited or STATUS_cur=='close'):  ##first case: Edge previous Valve or 'close'

                                    continue

                            '----------- current Edge(k) assessment ---------'
                            if FLAG_cur == '1':  ##case valve not assigned yet
                                    if list_path_a not in list_Paths:
                                            list_Paths.append(list_path_a)
                                            visited.add(EDGE_cur)
                                            list_edge_to_close.append(EDGE_cur)
                                            #
                                            Status_Edge_changed_with_dict(graph_Temp, EDGE_cur) #from 'open' to 'close' on EDGE_cur
                                            Remove_Edge_from_dict(graph_Temp,EDGE_cur)

                    '---------- Print temporary results and final result ----------'
##                    print('after for list_edge_to_close',list_edge_to_close)
##                    #if count_a==5:
##                    #        sys.exit()
##                    #print('path ending by valve')
##                    #print(list_path_a)
##                    #print('All Edges Visited : ',all_Edges_visited)
##                    print('---Pile Wastage on :',start[0])
##                    print('---Numbers of valves to close : ',len(list_edge_to_close))
##                    print('---List Edge to close : ',list_edge_to_close)
                    continue


        '-------------  Process neighbors for children of current Egde Unstacked ------------'

        Nb_neighbors_count=0
        Prev_EDGE_curr = EDGE_cur
        
        '------ loop over Neighbours for the Unstack Edge(k) ---------'
        for Current_neighbour_new in graph_Temp.get(EDGE_cur,[]):
                Nb_neighbors_count+=1
                # BFS Algo builts-up several paths neighbour node
                '-------------- Current Neighbor Edge --------------'
                s_current_Edge = Current_neighbour_new[0]
                s_current_Flag = Current_neighbour_new[1]
                s_current_Status = Current_neighbour_new[2]

                '------------- Read ID of Egde list_path_a for checking next row ----'
                a = list_path_a
                list_Edge_ID_s = [a[i][0] for i in range(len(a))]

                '------------- stack this Neighbour Edge if satisfies the conditions -----'
                if (s_current_Edge not in list_Edge_ID_s and s_current_Edge not in list_edge_to_close and s_current_Edge not in visited):
##                #KEEP ONLY LAST [EDGE,FLAG] both in list_stack and store unique Edges to all_Edges_visited
                        l_new_path = []
                        # after having built-up l_new_path
                        l_new_path.append(Current_neighbour_new) #Current_neighbour_new i with 3-uple list
                        if Current_neighbour_new not in all_Edges_visited:
                                list_stack.append((Current_neighbour_new,l_new_path))

    '--------  Print final result ------'
    print('---Pile Wastage on : ',start[0])
    print('---Numbers of valves to close : ',len(list_edge_to_close))
    print('---List Edges to close : ',list_edge_to_close)
    '----- output ------'
    return list_Paths


#-------------------------------------------------------------
#---------------------- RUNS WITH DFS  -----------------------
#-------------------------------------------------------------

#==========
##DFS based path finding
#==========
##### with dict_Node_Edges_Flag

##### with dict_Edges_Flag adjacency list of Edges
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T42','0','open'])    #done
l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14Td17-1','0','open']) #8 valves to close (done)
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T6a6','0','open'])   #done
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T533-1','0','open']) #done
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T8d0-2','0','open']) #done
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14Tdf3','0','open'])   #done
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T861','0','open'])   #done
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T9','0','open'])      #done
##print('l_Paths_endValve',l_Paths_endValve)#test for paths end valve
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_W_Flags,['14T117f-4','0','open']) #problem with change_Status



#------------------------  RUNETIME -----------------------------

#Running time test Algorithm BFS with n = Step (100,300,500,700,900,1100) , Delete comments if you want tot test the running time with output of Linear Graphic

'----------------------------------------------------'

#ta= time()
#
#Limit step for each implementation  = 100,300,500,700,900,1100
#Edges_to_close = dfs_paths_cycle(dict_Edges_W_Flags,['14T42','0','open'])

##print("---DFS 100 first  ---"'\n')
###
##dfs_result_append = set()
##for ii in range(20):
##        Edges_to_close = dfs_paths_cycle(dict_Edges_W_Flags,['14T42','0','open'])

#while len(dfs_result_append) < 100:
#    dfs_result_append.add(next(Edges_to_close))

#print (os.linesep.join(map(str,dfs_result_append)),'\n')
ta_end= time()
ta_time= (ta_end-ta)
print ('Time with 100 step : ',ta_time)

'----------------------------------------------------'

