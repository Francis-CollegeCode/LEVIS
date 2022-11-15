//Include headers and libraries
#include <iostream>
#include <fstream>
#include "LeptonThread.h"
#include <jsoncpp/json/json.h>
#include "Palettes.h"
#include "SPI.h"
#include "Lepton_I2C.h"

//for FIFO data transfer
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <sstream>

using namespace std;

#define PACKET_SIZE 164
#define PACKET_SIZE_UINT16 (PACKET_SIZE/2)
#define PACKETS_PER_FRAME 60
#define FRAME_SIZE_UINT16 (PACKET_SIZE_UINT16*PACKETS_PER_FRAME)
#define FPS 27;


LeptonThread::LeptonThread() : QThread()
{

	//
	typeColormap = 3; // 1:colormap_rainbow  /  2:colormap_grayscale  /  3:colormap_ironblack(default)
	selectedColormap = colormap_ironblack;
	selectedColormapSize = get_size_colormap_ironblack();

	//
	typeLepton = 2; // 2:Lepton 2.x  / 3:Lepton 3.x
	myImageWidth = 80;
	myImageHeight = 60;

	//
	spiSpeed = 20 * 1000 * 1000; // SPI bus speed 20MHz

	// min/max value for scaling
	autoRangeMin = true;
	autoRangeMax = true;
	rangeMin = 30000;
	rangeMax = 32000;
}

LeptonThread::~LeptonThread() {
}

void LeptonThread::setLogLevel(uint16_t newLoglevel)
{
	loglevel = newLoglevel;
}

void LeptonThread::useColormap(int newTypeColormap)
{
	switch (newTypeColormap) {
	case 1:
		typeColormap = 1;
		selectedColormap = colormap_rainbow;
		selectedColormapSize = get_size_colormap_rainbow();
		break;
	case 2:
		typeColormap = 2;
		selectedColormap = colormap_grayscale;
		selectedColormapSize = get_size_colormap_grayscale();
		break;
	default:
		typeColormap = 3;
		selectedColormap = colormap_ironblack;
		selectedColormapSize = get_size_colormap_ironblack();
		break;
	}
}

void LeptonThread::useLepton(int newTypeLepton) //flags Lepton model number
{
	switch (newTypeLepton) {
	case 3:
		typeLepton = 3;
		myImageWidth = 160;
		myImageHeight = 120;
		break;
	default:
		typeLepton = 2;
		myImageWidth = 80;
		myImageHeight = 60;
	}
}

void LeptonThread::useSpiSpeedMhz(unsigned int newSpiSpeed)
{
	spiSpeed = newSpiSpeed * 1000 * 1000;
}

void LeptonThread::setAutomaticScalingRange()
{
	autoRangeMin = true;
	autoRangeMax = true;
}

void LeptonThread::useRangeMinValue(uint16_t newMinValue)
{
	autoRangeMin = false;
	rangeMin = newMinValue;
}

void LeptonThread::useRangeMaxValue(uint16_t newMaxValue)
{
	autoRangeMax = false;
	rangeMax = newMaxValue;
}

//used in run() for fifo conversions
string convertToString(char* a, int size){
string s = "";
for (int i = 0; i < size; i++) {
	s = s + a[i];
}
return s;
}

void LeptonThread::run()
{
	//set flag for ending the Lepton Camera
	//bool passed = false;
	int m = 0;
	int n = 0;
	int number;
	int xArray[5];
	int yArray[5];
	bool xy = true;
	bool fifoClose = false;
	bool noseRead = false;
	
	
	string delimiter = ".";
	size_t pos = 0;
	string token;
	
    int myfile;

    // FIFO file path
    char * myfifo = "/home/pi/Desktop/LEVIS/Camera/Both/StreamCapture/mypipe";

    // Creating the named file(FIFO)

	//char image_name[32];
	//int image_index = 0;
	
	//create the initial image
	myImage = QImage(myImageWidth, myImageHeight, QImage::Format_RGB888);

	const int *colormap = selectedColormap;
	const int colormapSize = selectedColormapSize;
	uint16_t minValue = rangeMin;
	uint16_t maxValue = rangeMax;
	float diff = maxValue - minValue;
	float scale = 255/diff;
	uint16_t n_wrong_segment = 0;
	uint16_t n_zero_value_drop_frame = 0;

	//open spi port
	SpiOpenPort(0, spiSpeed);
	
	//creating a csv file to store temps
	FILE *out_file  = fopen("all_temps.csv", "w+");
	int truePixValue = 0;
	
	while(!fifoClose){
		//BEGIN FIFO READ
		// mkfifo(<pathname>,<permission>) 0666 means all can read
		mkfifo(myfifo, 0666);

		char message[80];
		while (noseRead == false){	
			m = 0;
			n = 0;
			// First open in read only and read
			myfile = open(myfifo,O_RDONLY);
			read(myfile, message, 80);

			//Print the read string and close
			//printf("message: %s\n", message);
		
			//coverting char array into string
			int message_size = sizeof(message) / sizeof(char);
			string messageString = convertToString(message, message_size);
			//cout << "String: " + messageString << endl;

		//Parse string
			while ((pos = messageString.find(delimiter)) != std::string::npos) {
				token = messageString.substr(0, pos);
				
				//turning parsed strings into ints
				stringstream converter(token);
				converter >> number;
				//cout << "Printing int: " << number << endl;	//prints ints
				//cout << token << endl;		//prints strings
				if (number == 69420){
					cout << "closed fifo" << endl;
					noseRead = true;
					fifoClose = true;
					close(myfile);
					break;
				}
				else if (number == 42069){
					/*			
					for(int k = 0; k < 5; k++){
						cout << "X-Array " << k << " " << xArray[k] << endl;
					}
					for(int d = 0; d < 5; d++){
						cout << "Y-Array " << d << " " << yArray[d] << endl;
					}
					*/
					noseRead = true;	
					break;
				}	
				
				if (xy == true){
					xArray[m] = number;	
					xy = false;
					m++;
				}	
				else if (xy == false){
					yArray[n] = number;	
					xy = true;
					n++;
				}	
					
				
				messageString.erase(0, pos + delimiter.length());
				
			} // end parsing strings
		} //end fifo loop
		//END FIFO READ
		if(fifoClose == false){
			//read data packets from lepton over SPI
			int resets = 0;
			int segmentNumber = -1;
			//SPI READ LOOP
			for(int j=0;j<PACKETS_PER_FRAME;j++) {
				//if it's a drop packet, reset j to 0, set to -1 so he'll be at 0 again loop
				read(spi_cs0_fd, result+sizeof(uint8_t)*PACKET_SIZE*j, sizeof(uint8_t)*PACKET_SIZE);
				int packetNumber = result[j*PACKET_SIZE+1];
				if(packetNumber != j) {
					j = -1;
					resets += 1;
					usleep(1000);
					//Note: we've selected 750 resets as an arbitrary limit, since there should never be 750 "null" packets between two valid transmissions at the current poll rate
					//By polling faster, developers may easily exceed this count, and the down period between frames may then be flagged as a loss of sync
					if(resets == 750) {
						SpiClosePort(0);
						lepton_reboot();
						n_wrong_segment = 0;
						n_zero_value_drop_frame = 0;
						usleep(750000);
						SpiOpenPort(0, spiSpeed);
					}
					continue;
				}//CHECK INVALID PACKET NUMBER
				if ((typeLepton == 3) && (packetNumber == 20)) { //version-specific errors if the Lepton is a 3.x, the breaks the loop after
					segmentNumber = (result[j*PACKET_SIZE] >> 4) & 0x0f;
					if ((segmentNumber < 1) || (4 < segmentNumber)) {
						log_message(10, "[ERROR] Wrong segment number " + std::to_string(segmentNumber));
						break;
					}
				}
			}//END OF SPI READ LOOP
			
			if(resets >= 30) {
				log_message(3, "done reading, resets: " + std::to_string(resets));
			}


			//
			int iSegmentStart = 1;
			int iSegmentStop;
			if (typeLepton == 3) {
				if ((segmentNumber < 1) || (4 < segmentNumber)) {
					n_wrong_segment++;
					if ((n_wrong_segment % 12) == 0) {
						log_message(5, "[WARNING] Got wrong segment number continuously " + std::to_string(n_wrong_segment) + " times");
					}
					continue;
				}
				if (n_wrong_segment != 0) {
					log_message(8, "[WARNING] Got wrong segment number continuously " + std::to_string(n_wrong_segment) + " times [RECOVERED] : " + std::to_string(segmentNumber));
					n_wrong_segment = 0;
				}

				memcpy(shelf[segmentNumber - 1], result, sizeof(uint8_t) * PACKET_SIZE*PACKETS_PER_FRAME);
				if (segmentNumber != 4) {
					continue;
				}
				iSegmentStop = 4;
			}
			else {
				memcpy(shelf[0], result, sizeof(uint8_t) * PACKET_SIZE*PACKETS_PER_FRAME);
				iSegmentStop = 1;
			}

			if ((autoRangeMin == true) || (autoRangeMax == true)) {
				if (autoRangeMin == true) {
					maxValue = 65535;
				}
				if (autoRangeMax == true) {
					maxValue = 0;
				}
				for(int iSegment = iSegmentStart; iSegment <= iSegmentStop; iSegment++) {
					for(int i=0;i<FRAME_SIZE_UINT16;i++) {
						//skip the first 2 uint16_t's of every packet, they're 4 header bytes
						if(i % PACKET_SIZE_UINT16 < 2) {
							continue;
						}

						//flip the MSB and LSB at the last second
						uint16_t value = (shelf[iSegment - 1][i*2] << 8) + shelf[iSegment - 1][i*2+1];
						if (value == 0) {

							continue;
						}
						if ((autoRangeMax == true) && (value > maxValue)) {
							maxValue = value;
						}
						if ((autoRangeMin == true) && (value < minValue)) {
							minValue = value;
						}
					}
				}
				diff = maxValue - minValue;
				scale = 255/diff;
			}
			//image variables
			int row, column;
			uint16_t value;
			uint16_t valueFrameBuffer;
			QRgb color;
			//This is where the image is set and the nose coordinate values are read
			for(int iSegment = iSegmentStart; iSegment <= iSegmentStop; iSegment++) {
				int ofsRow = 30 * (iSegment - 1);
				for(int i=0;i<FRAME_SIZE_UINT16;i++) {
					//skip the first 2 uint16_t's of every packet, they're 4 header bytes
					if(i % PACKET_SIZE_UINT16 < 2) {
						continue;
					}

					//flip the MSB and LSB at the last second
					valueFrameBuffer = (shelf[iSegment - 1][i*2] << 8) + shelf[iSegment - 1][i*2+1];
					if (valueFrameBuffer == 0) {

						n_zero_value_drop_frame++;
						if ((n_zero_value_drop_frame % 12) == 0) {
							log_message(5, "[WARNING] Found zero-value. Drop the frame continuously " + std::to_string(n_zero_value_drop_frame) + " times");
						}
						break;
					}

					value = (valueFrameBuffer - minValue) * scale;
					int ofs_r = 3 * value + 0; if (colormapSize <= ofs_r) ofs_r = colormapSize - 1;
					int ofs_g = 3 * value + 1; if (colormapSize <= ofs_g) ofs_g = colormapSize - 1;
					int ofs_b = 3 * value + 2; if (colormapSize <= ofs_b) ofs_b = colormapSize - 1;
					color = qRgb(colormap[ofs_r], colormap[ofs_g], colormap[ofs_b]);
					if (typeLepton == 3) {
						column = (i % PACKET_SIZE_UINT16) - 2 + (myImageWidth / 2) * ((i % (PACKET_SIZE_UINT16 * 2)) / PACKET_SIZE_UINT16);
						row = i / PACKET_SIZE_UINT16 / 2 + ofsRow;
					}
					else {
						column = (i % PACKET_SIZE_UINT16) - 2;
						row = i / PACKET_SIZE_UINT16;
					}
					myImage.setPixel(column, row, color);
					
					//Storing temps into variables
					double tempK = (double)valueFrameBuffer/100;
					double tempF = ((tempK-273.15)*9/5)+32;
					
					//Storing temps into a csv file
					if (truePixValue%160 == 0 && truePixValue > 0){	//<- This should happen 119 times and print 1-119
						fprintf(out_file, "\n");
					}
					fprintf(out_file, "%f,", tempF);
					
					truePixValue++;
					
					QRgb c = qRgb(0, 255, 0); //Makes the green for the picture
					for (int j = 0; j<5;j++){
						//printf("column: %d  row %d\n", column, row);
						if (row == xArray[j] && column == yArray[j]){ //xArray[i].asInt(), yArray[i].asInt()
							if (j == 0)
								printf("\n");
							
							printf("Pixel (%d, %d) = %.2f K, or %.2f F      \n", row,column,tempK,tempF);	
							myImage.setPixel(row,column, c);	
						}
						
					}
					
					
					
				}
			}

			if (n_zero_value_drop_frame != 0) {
				log_message(8, "[WARNING] Found zero-value. Drop the frame continuously " + std::to_string(n_zero_value_drop_frame) + " times [RECOVERED]");
				n_zero_value_drop_frame = 0;
			}

			//lets emit the signal for update
			emit updateImage(myImage);
			noseRead = false;
			
			//then capture updated image
			/*
			do {
			sprintf(image_name, "Screenshot_%.3d.jpg", image_index);
			image_index += 1;
			if (image_index > 999) 
			{
				image_index = 0;
				break;
			}

			} while (access(image_name, F_OK) == 0);
			*/
		}
	}
	
	//finally, close SPI port just bcuz
	SpiClosePort(0);
	QCoreApplication::exit(0);
}

void LeptonThread::performFFC() {
	//perform FFC
	lepton_perform_ffc();
}

void LeptonThread::log_message(uint16_t level, std::string msg)
{
	if (level <= loglevel) {
		std::cerr << msg << std::endl;
	}
}

