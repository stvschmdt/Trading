#include "headers.h"
#include "share.h"
#include "database.h"
/*master todo

create vector of Entry objects representing rows of data of a share
read into memory full data set
sqlite db to store transactions and simulations

*/


void error(const char * msg){
    std::cout<< "[error] " << msg << std::endl;
}

void usage(){
    std::cout<< " ./program [config_file_path] [is_live]" << std::endl;
}

/*read command line arguments - handle passing global variables to executive*/
int handle_cli(int len, char ** args){
    try{
        char *CONFIG=args[1];
        char *IS_LIVE=args[2];
        Database db = Database();
         
    }
    catch(const std::exception& e){
       error("argument parsing / assignment failed");
        
    }
    return 0;

}


/*dummy harness - turn this into unit tests later - use for testing objects*/
void testHarness(){
    /*test share class*/
    Share goog = Share("goog");
    std::cout<<goog.getSymbol()<<std::endl;
    goog.readCsv("../data/2015_curr/AAPL.csv");
    goog.formatData();
    goog.showData();
}   

/*main entry point - handle command line arguments, usage, parameter file checking*/
int main(int argc, char ** argv){
	std::cout<<"beginning Trading simulation"<<std::endl;
    if( argc < 3) {
        usage();
    }
    else{
        handle_cli(argc, argv);
        /*test harness for now*/
        testHarness();
    }  
	return 0;
}
