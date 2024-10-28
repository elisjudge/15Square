class Game {
    constructor({
        board = document.getElementById("board"),
        tiles = [],
        rows = 4,
        columns = 4
        
        } = {}) {
        this.board = {
            gameBoard: board,
            isShuffled: false,
        };
        this.tiles = tiles;
        this.winningTiles = [];
        this.winner = false;
        this.rows = rows;
        this.columns = columns;
        this.init();
    }

    init() {
        for (let i = 0; i < this.rows; i++) {
            let row = document.createElement("div");
            row.className = "row";
            for (let j = 0; j < this.columns; j++) {
                let cell = document.createElement("div");
                let index = i * 4 + j + 1;
                
                cell.className = "tile";

                cell.dataset.index = index;
                cell.dataset.value = index;
                cell.textContent = index === 16 ? "" : index;

                row.appendChild(cell);
                this.tiles.push(cell);  // Store tile reference
                this.winningTiles.push(index); // Store index value
            }
            this.board.gameBoard.appendChild(row);
        }


        // Shuffle tiles 
        for (let i = 0; i < 1000; i++) {
            this.click({ 
                target: { 
                    dataset: {
                      index: Math.floor(Math.random() * 15) + 1   
                    }
                }
            });
        }
        this.board.isShuffled = true;


        this.tiles.forEach((tile) => {
            tile.addEventListener("click", (event) => {
                if (!this.winner) {
                    this.click(event);
                }
            });
        });
    }

    click(e) {
        let i = parseInt(e.target.dataset.index, 10) - 1;

        if (i - 4 >= 0 && this.tiles[i - 4].dataset.value === "16") {
            this.swap(i, i - 4);
        } else if (i + 4 < 16 && this.tiles[i + 4].dataset.value === "16") {
            this.swap(i, i + 4);
        } else if (i % 4 !== 0 && this.tiles[i - 1].dataset.value === "16") {
            this.swap(i, i - 1);
        } else if (i % 4 !== 3 && this.tiles[i + 1].dataset.value === "16") {
            this.swap(i, i + 1);
        }
        
        if (this.board.isShuffled) {
            this.checkWin();
        }
    }

    swap(i, j) {
        let temp = this.tiles[i].dataset.value;
        this.tiles[i].textContent = this.tiles[j].textContent;
        this.tiles[i].dataset.value = this.tiles[j].dataset.value;
        this.tiles[j].textContent = temp === "0" ? "" : temp;
        this.tiles[j].dataset.value = temp;
    }

    checkWin() {
        for (let i = 0; i < this.tiles.length; i++){
            if (this.tiles[i].dataset.value != this.winningTiles[i]) {
                console.log("Not yet");
                return;
            }
        }
        console.log("you win");
        this.winner = true;
        this.tiles[this.tiles.length -1].textContent = "16"
    }
}

// Instantiate Game once DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    const game = new Game();
});
