export class Mod {
    public title: string;
    public author?: string;
    public releaseDate?: Date;

    constructor(title: string, author?: string, releaseDate?: Date) {
        this.title = title;

        if (author){
          this.author = author;
        } else {
          this.author = "No author set.";
        }

        if (releaseDate) {
            this.releaseDate = releaseDate;
        } else {
            this.releaseDate = null;
        }

        if (!(releaseDate instanceof Date)) {
            throw new Error('Date is not a valid Date Object');
        }
    }
}
