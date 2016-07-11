#include "headers.h"
#include "share.h"
#include "database.h"
#include "entry.h"
/*master todo

creater parameter file reader [main.cpp]

*/


void error(const char * msg){
    std::cout<< "[error] " << msg << std::endl;
}

void usage(){
    std::cout<< " ./program [config_file_path] [is_live]" << std::endl;
}

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

void testHarness(){
    /*test share class*/
    Share goog = Share("goog");
    std::cout<<goog.getSymbol()<<std::endl;

}   

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
