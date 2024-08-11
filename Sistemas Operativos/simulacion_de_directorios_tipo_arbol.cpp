#include <bits/stdc++.h>

using namespace std;

class Nodo {
public:
    string nombre;
    time_t tiempo_modificado;
    bool es_directorio;
    Nodo* padre;
    vector<Nodo*> hijos;

    Nodo(string nombre, bool es_directorio) : nombre(nombre), es_directorio(es_directorio), padre(nullptr) {
        time(&tiempo_modificado);
    }
    ~Nodo() {
        for (Nodo* hijo : hijos) {
            delete hijo;
        }
    }
    void actualizar_tiempo_modificado() {
        time(&tiempo_modificado);
    }
};

class SistemaArchivos {
public:
    SistemaArchivos() {
        raiz = new Nodo("/Mael", true);
        actual = raiz;
    }

    ~SistemaArchivos() {
        delete raiz;
    }

    void mostrar_directorio_actual() {
        cout << obtener_ruta(actual) << endl;
    }

    void listar_directorio() {
        for (Nodo* nodo : actual->hijos) {
            cout << (nodo->es_directorio ? "D" : "F") << " " << nodo->nombre << endl;
        }
    }

    void cambiar_directorio(const string& nombre_dir) {
        if (nombre_dir == "..") {
            if (actual->padre != nullptr) {
                actual = actual->padre;
            }
        } else {
            Nodo* dir = encontrar_nodo(nombre_dir);
            if (dir && dir->es_directorio) {
                actual = dir;
            } else {
                cout << "Directorio no encontrado." << endl;
            }
        }
    }

    void copiar_nodo(const string& nombre_origen, const string& nombre_destino) {
        Nodo* origen = encontrar_nodo(nombre_origen);
        if (origen) {
            Nodo* copia = copiar_recursivo(origen);
            copia->nombre = nombre_destino;
            actual->hijos.push_back(copia);
            copia->padre = actual;
        } else {
            cout << "Origen no encontrado." << endl;
        }
    }

    void mover_nodo(const string& nombre_origen, const string& nombre_destino) {
        Nodo* origen = encontrar_nodo(nombre_origen);
        if (origen) {
            origen->nombre = nombre_destino;
        } else {
            cout << "Origen no encontrado." << endl;
        }
    }

    void eliminar_nodo(const string& nombre) {
        auto it = remove_if(actual->hijos.begin(), actual->hijos.end(),[&nombre](Nodo* nodo){return nodo->nombre == nombre;});
        if (it != actual->hijos.end()) {
            delete *it;
            actual->hijos.erase(it, actual->hijos.end());
        }
        else
            cout << "Nodo no encontrado." << endl;
    }

    void crear_archivo(const string& nombre) {
        Nodo* archivo = new Nodo(nombre, false);
        archivo->padre = actual;
        actual->hijos.push_back(archivo);
    }

    void actualizar_tiempo_archivo(const string& nombre) {
        Nodo* archivo = encontrar_nodo(nombre);
        if (archivo && !archivo->es_directorio)
            archivo->actualizar_tiempo_modificado();
        else
            cout << "Archivo no encontrado." << endl;
    }

    void crear_directorio(const string& nombre) {
        Nodo* dir = new Nodo(nombre, true);
        dir->padre = actual;
        actual->hijos.push_back(dir);
    }

    void eliminar_directorio_vacio(const string& nombre) {
        Nodo* dir = encontrar_nodo(nombre);
        if (dir && dir->es_directorio && dir->hijos.empty()) {
            auto it = remove(actual->hijos.begin(), actual->hijos.end(), dir);
            delete dir;
            actual->hijos.erase(it, actual->hijos.end());
        }
        else
            cout << "Directorio no encontrado o no esta vacio." << endl;
    }

    void buscar(const string& nombre) {
        buscar_recursivo(raiz, nombre);
    }

    void buscar_texto(const string& texto) {
        cout << "Busqueda de texto no implementada." << endl;
    }

    void mostrar_info(const string& nombre) {
        Nodo* nodo = encontrar_nodo(nombre);
        if (nodo) {
            cout << (nodo->es_directorio ? "Directorio: " : "Archivo: ") << nodo->nombre << endl;
            cout << "ultima modificacion: " << ctime(&nodo->tiempo_modificado);
            if (nodo->es_directorio)
                cout << "Contenido: " << nodo->hijos.size() << " elementos" << endl;
        }
        else
            cout << "Nodo no encontrado." << endl;
    }

private:
    Nodo* raiz;
    Nodo* actual;

    Nodo* encontrar_nodo(const string& nombre) {
        for (Nodo* nodo : actual->hijos) {
            if (nodo->nombre == nombre)
                return nodo;
        }
        return nullptr;
    }

    Nodo* copiar_recursivo(Nodo* origen) {
        Nodo* copia = new Nodo(*origen);
        for (Nodo* hijo : origen->hijos) {
            Nodo* hijo_copia = copiar_recursivo(hijo);
            copia->hijos.push_back(hijo_copia);
            hijo_copia->padre = copia;
        }
        return copia;
    }

    void buscar_recursivo(Nodo* nodo, const string& nombre) {
        if (nodo->nombre.find(nombre) != string::npos)
            cout << obtener_ruta(nodo) << endl;
        for (Nodo* hijo : nodo->hijos)
            buscar_recursivo(hijo, nombre);
    }

    string obtener_ruta(Nodo* nodo) {
        if (nodo->padre == nullptr)
            return nodo->nombre;
        return obtener_ruta(nodo->padre) + "/" + nodo->nombre;
    }
};

int main() {
    SistemaArchivos fs;
    string comando, nombre, nombre2;

    while (true) {
        fs.mostrar_directorio_actual();
        cout << "$ ";
        cin >> comando;

        if (comando == "ls") {
            fs.listar_directorio();
        } else if (comando == "cd") {
            cin >> nombre;
            fs.cambiar_directorio(nombre);
        } else if (comando == "cp") {
            cin >> nombre >> nombre2;
            fs.copiar_nodo(nombre, nombre2);
        } else if (comando == "mv") {
            cin >> nombre >> nombre2;
            fs.mover_nodo(nombre, nombre2);
        } else if (comando == "rm") {
            cin >> nombre;
            fs.eliminar_nodo(nombre);
        } else if (comando == "touch") {
            cin >> nombre;
            fs.crear_archivo(nombre);
        } else if (comando == "utime") {
            cin >> nombre;
            fs.actualizar_tiempo_archivo(nombre);
        } else if (comando == "mkdir") {
            cin >> nombre;
            fs.crear_directorio(nombre);
        } else if (comando == "rmdir") {
            cin >> nombre;
            fs.eliminar_directorio_vacio(nombre);
        } else if (comando == "find") {
            cin >> nombre;
            fs.buscar(nombre);
        } else if (comando == "show") {
            cin >> nombre;
            fs.mostrar_info(nombre);
        } else if (comando == "cls") {
            system("cls");
        } else if (comando == "exit") {
            break;
        } else {
            cout << "Comando desconocido." << endl;
        }
    }

    return 0;
}
