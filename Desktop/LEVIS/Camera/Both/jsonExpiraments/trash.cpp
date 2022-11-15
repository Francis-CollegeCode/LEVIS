#include <iostream>
#include <fstream>
#include <jsoncpp/json/json.h>

using namespace std;

int main(){

	ifstream ifs("trash.json");
	Json::Reader reader;
	Json::Value obj;
	reader.parse(ifs, obj);
	cout << "LastName: " << obj["lastname"].asString() << endl;
	cout << "FirstName: " << obj["firstname"].asString() << endl;
	cout << "SS: " << obj["ss"].asInt() << endl;
	return 1;
	
}
