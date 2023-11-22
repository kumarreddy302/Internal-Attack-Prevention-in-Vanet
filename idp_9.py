import xml.etree.ElementTree as ET


def extract_first_edge_from_xml(xml_file, target_route_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    route_edges = {}
    for route in root.findall('route'):
        route_id = route.attrib.get('id')
        if route_id == target_route_id:
            edges = route.attrib.get('edges')
            edges_list = edges.split()
            ##print(edges_list)  
            return edges_list


def determine_direction(edge):
    if '#0_0' in edge:
        return "You can take a left turn or continue on the same lane."
    elif '#1_' in edge or '#3_' in edge:
        return "You can take a right turn or continue on the same lane."
    elif '#2_' in edge:
        return "You can continue on the same lane or switch lanes left."
   ### else:
    ###    return "You can continue on the same lane."
    ###

def make_decision(current_edge, user_decision,trustscore):
    if user_decision.lower() == 'left':
        if current_edge.endswith('#0'):
            print("You can take a left turn.")
        else:
            print("You can't make a left turn")
            trustscore = trustscore - 10
    elif user_decision.lower() == 'swr':        
        if current_edge.endswith('#0') or current_edge.endswith('#1') or current_edge.endswith('#2'):
            print("You can switch lanes right.")
        else:
            print("Right Lane swift is not possible based on the edge.")
            trustscore = trustscore - 10
    elif user_decision.lower() == 'swl':        
        if current_edge.endswith('#1') or current_edge.endswith('#2') or current_edge.endswith('#3'):
            print("You can switch lanes left.")
        else:
            print("Left turn is not possible based on the edge.")
            trustscore = trustscore - 10        
    elif user_decision.lower() == 'right':
        if current_edge.endswith('#1') or current_edge.endswith('#3') :
            print("You can take a right turn.")
        else:    
            print("Right turn is not possible based on the edge.")
            trustscore = trustscore - 10
    elif user_decision.lower() == 'same lane':
        print("You chose to continue on the same lane.")
    elif user_decision.lower() == 'exit':
        print("Exiting route navigation.")
        exit()
    else:
        print("Invalid input. Please enter 'left', 'right', 'same lane','swl(switch lane left)','swr(switch lane right)' or 'exit'.")
    return trustscore

def get_next_edge(current_edge):
    current_edge_index = current_edge.find('_')
    if current_edge_index == -1:
        return None  # Reached the end of the route

    next_edge_index = current_edge_index + 1
    if next_edge_index == len(current_edge):
        return None  # Reached the end of the route

    next_edge_value = current_edge[next_edge_index:]
    return next_edge_value


def main():
    xml_file_path = 'fun.xml'
    trustscore = 100
    target_route_id = input("Enter the target route ID: ")
    while trustscore > 70 :
        route_edges = extract_first_edge_from_xml(xml_file_path, target_route_id)
        for uj in route_edges:
            if route_edges:
                current_edge = uj

                while current_edge and trustscore > 70:
                    # Display the current edge
                    print(f"Current edge: {current_edge}")

                # Determine the direction based on the current edge
                    direction = determine_direction(current_edge)
                    print(f"Direction: {direction}")

                # Prompt the user for their decision
                    user_decision = input("Enter your decision (left, right, same lane,swl(switch lane left),swr(switch lane right) or exit): ")

                # Make a decision based on the user's input
                    trustscore = make_decision(current_edge, user_decision,trustscore)
                    
                # Update the current edge to the next one
                    next_edge = get_next_edge(current_edge)
                    current_edge = next_edge

                    if not current_edge:
                        ##print("You have reached the end of the route.")
                        break

            else:
                print(f"Route ID '{target_route_id}' not found in the XML file.")
    else :
        print("You are are an Internal Attacker.We can't take your commands")

if __name__ == '__main__':
    main()
