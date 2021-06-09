#include <iostream>
#include <fstream>
#include <string>

// g++ selection_base_SIRENE.cpp -o selection_base_SIRENE && ./selection_base_SIRENE

int main(){

    std::cout << "Début de la lecture" << std::endl;

    std::ifstream file_in("../../data/base_sirene_shortened.json");

    std::string fichier_complet;

    getline(file_in, fichier_complet);

    file_in.close();

    std::cout << "Lecture finie" << std::endl;
    std::cout << "Début de la réduction" << std::endl;

    
    int brackets_count = 0; 
    int i = 0;

    std::string fichier_reduit = "";

    while (brackets_count <= 200000){
        fichier_reduit += fichier_complet[i];
        
        if (fichier_complet[i] == '}'){ 
            brackets_count++;
        }

        i++;
    }

    fichier_reduit += "]";

    std::cout << "Réduction finie" << std::endl;
    std::cout << "Début de l'écriture" << std::endl;

    std::ofstream file_out("output/Sirene_100000.json");

    file_out << fichier_reduit;

    file_out.close();
    
    std::cout << "Ecriture finie" << std::endl;

    return 0;
}