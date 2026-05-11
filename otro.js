
class GestorNomina {
    constructor(pagoHora) {
        this.pagoHora = pagoHora;
    }

    calcular = (fila) => { //flecha 
        let normales = 0;
        let extras = 0;
        
        
        for (let i = 0; i < fila.length; i++) {
            if (fila[i] === 1) normales++;
            else if (fila[i] === 2) extras++;
        }

        const total = (normales * this.pagoHora) + (extras * this.pagoHora * 1.5);
        return { total, normales, extras };
    }
}

const nombres = ["Juan", "Lizeth", "Cristina"];
const miGestor = new GestorNomina(20);

let matrizAsistencia = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 2],
    [1, 1, 0, 0, 1, 1, 1, 1, 0]
];

const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

const mostrarMenu = () => {
    console.log("\nSISTEMA ");
    console.table(matrizAsistencia);
    console.log("\n  0= ------Juan------");
    console.log("\n  1= ------Lizeth------");
    console.log("\n  2= ------Cristina------");
    console.log("1. Modificar | 2. Reporte | 3. Salir");
    
    readline.question("\nSelección: ", (opcion) => {
        if (opcion === "1") modificar();
        else if (opcion === "2") reporte();
        else if (opcion === "3") {
            console.log("Fin.");
            readline.close();
        } else mostrarMenu();
    });
};
const modificar = () => {//otra
    readline.question("persona (0-2): ", (id) => {
        readline.question("Hora (0-8): ", (col) => {
            readline.question("Valor (0,1,2): ", (val) => {
                const i = parseInt(id);
                const j = parseInt(col);
                const v = parseInt(val);

                if (matrizAsistencia[i] && matrizAsistencia[i][j] !== undefined) {
                    matrizAsistencia[i][j] = v;
                    console.log("Actualizado.");
                }
                mostrarMenu();
            });
        });
    });
};

const reporte = () => {//ultima
    console.log("\n--- PAGOS CALCULADOS ---");
    matrizAsistencia.forEach((fila, i) => {
        const res = miGestor.calcular(fila);
        console.log(`${nombres[i]}: $${res.total}`);
    });
    mostrarMenu();
};


mostrarMenu();














//easter egg 