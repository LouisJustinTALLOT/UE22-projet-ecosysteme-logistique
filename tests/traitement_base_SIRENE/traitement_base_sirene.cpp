#include <iostream>
#include <fstream>
#include <string>
#include <chrono>

// g++ traitement_base_sirene.cpp -o traitement_base_sirene && ./traitement_base_sirene

int main() {
    ////////////////// lecture du fichier source //////////////////

    std::chrono::time_point<std::chrono::high_resolution_clock> start, end;

    // std::string input_filename = "base-sirene.json";
    std::string input_filename = "base_sirene_extrait_travail.json";
    std::string output_filename = "base_sirene_shortened_json_cpp.json";

    std::ifstream file_in(input_filename);

    std::string input_text;

    start = std::chrono::high_resolution_clock::now();
    getline(file_in, input_text);

    end = std::chrono::high_resolution_clock::now();
    file_in.close();

    std::cout << "lecture finie en ";
    std::cout << (end - start).count() / 1000000000.0 << " secondes" << std::endl;

    ////////////////// début du traitement //////////////////
    start = std::chrono::high_resolution_clock::now();
    /*
     * traitement fini en 62 secondes en faisant auto car : input_text
     * et en 52 secondes en faisant int i = 0; i < input_text.size(); i++
     */
    // std::ofstream file_out(output_filename);

    std::string output_text = "[";
    // file_out << output_text;
    int nombre_entrees = 0;

    int input_length = int(input_text.size());
    std::cout << "taille du texte d'entrée : " << input_length << std::endl;

    for (int i = 1; i < input_length - 10; i++) {
        if (input_text.substr(i, 8) == "recordid") {
        } 
        
        else if (input_text.substr(i, 8) == "record_t") {

            if (i + 50 < input_length) {
            }

            output_text += "{";
            nombre_entrees++;
            i += 750;
        }

            output_text += "}";
                output_text += ",";
            }


        // if (nombre_entrees > 10) {
        //     break;
        // }
    }

    output_text += "]";

    end = std::chrono::high_resolution_clock::now();

    std::cout << "traitement fini en ";
    std::cout << (end - start).count() / 1000000000.0 << " secondes" << std::endl;

    ////////////////// écriture du résultat dans un fichier abrégé //////////////////
    start = std::chrono::high_resolution_clock::now();

    std::ofstream file_out(output_filename);

    file_out << output_text;

    file_out.close();

    end = std::chrono::high_resolution_clock::now();

    std::cout << "écriture au fichier résultat en ";
    std::cout << (end - start).count() / 1000000000.0 << " secondes" << std::endl;

    std::cout << std::endl
              << nombre_entrees << std::endl;
    return 0;
}