/*To run:
cd /home/pi/Desktop/LEVIS/Camera/Both
g++ -o ReadJson ReadJson.cpp -ljsoncpp
./ReadJson
*/


#include <jsoncpp/json/json.h>
#include <iostream>
#include <fstream>

using namespace std;

int main(){
	
	ifstream coordData("CoordinateData.json");
	Json::Reader reader;
	Json::Value coords;
	reader.parse(coordData,coords);
	
	auto xArray = coords["x-coordinates"];
	auto yArray = coords["y-coordinates"];
	
	for (int i = 0; i < 5; i++) {
		cout << xArray[i].asInt() << " " << yArray[i].asInt() << endl;
	}

	return 1;
	
}
