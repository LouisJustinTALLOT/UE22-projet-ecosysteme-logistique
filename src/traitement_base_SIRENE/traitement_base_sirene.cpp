#include <iostream>
#include <fstream>
#include <string>
#include <chrono>

// g++ traitement_base_sirene.cpp -o traitement_base_sirene && ./traitement_base_sirene

/**
 * @brief Traite la base SIRENE (fichier JSON de 1,7 Go) et en extrait les informations utiles
 * 
 * @return int 
 */
int main() {
    std::cout << "début du programme" << std::endl;
    ////////////////// lecture du fichier source //////////////////

    std::chrono::time_point<std::chrono::high_resolution_clock> start, end;

    std::string input_filename = "base-sirene.json";
    // std::string input_filename = "base_sirene_extrait_travail.json";
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

    std::string output_text = "[";

    std::string tmp = "";
    bool in_a_record = false;

    bool has_geometry = false;
    bool has_apet700 = false;
    bool has_libtefet = false;

    int nombre_entrees = 0;

    int input_length = int(input_text.size());
    std::cout << "taille du texte d'entrée : " << input_length << std::endl;

    for (int i = 1; i < input_length - 10; i++) {
        if (input_text.substr(i, 8) == "recordid") {
            tmp += "{";
            in_a_record = true;
        } 
        
        else if (input_text.substr(i,8) == "\"apet700") {

            has_apet700 = true;

            if (has_libtefet) {
                tmp += ",";
            }
            
            while (input_text[i] != ',') {
                if (input_text[i] != ' '){
                    tmp += input_text[i];
                }

                i++;
            }
        } 

        else if (input_text.substr(i, 9) == "\"libtefet") {
            has_libtefet = true;

            if (has_apet700) {
                tmp += ",";
            }

            while (input_text[i] != ',') {
                if (input_text[i] != ' '){
                    tmp += input_text[i];
                }

                i++;
            }
        }

        else if (input_text.substr(i, 9) == "\"geometry") {
            has_geometry = true;

            if (has_apet700 || has_libtefet) {
                tmp += ",";
            }

            while (input_text[i] != '}') {
                if (input_text[i] != ' '){
                    tmp += input_text[i];
                }

                i++;
            }
            tmp += "}";
        }

        else if (input_text.substr(i, 8) == "record_t") {
            tmp += "}";

            if (i + 50 < input_length) {
                tmp += ",";
            }

            // commenté pour l'instant
            if (true) {
            // if (has_geometry && has_apet700) {
                output_text += tmp;
            } else {
                tmp = "";
            }

            tmp = "";
            in_a_record = false;
            has_geometry = false;
            has_apet700 = false;
            has_libtefet = false;
            nombre_entrees++;
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