export class Mod {
    public title: string;
    public author: string;
    public releaseDate: Date;

    constructor(title: string, author: string, releaseDate: Date) {
        this.title = title;
        this.author = author;
        this.releaseDate = releaseDate
        
        if (!typeof releaseDate === Date) {
            return new Error('Date is not a valid Date Object');
        }
    }
}