import { LitElement } from 'lit';
export declare class MGnifySourmash extends LitElement {
    directory: boolean;
    show_directory_checkbox: boolean;
    show_signatures: boolean;
    num: number;
    ksize: number;
    is_protein: boolean;
    dayhoff: boolean;
    hp: boolean;
    seed: number;
    scaled: number;
    track_abundance: boolean;
    selectedFiles: Array<File>;
    progress: {
        [filename: string]: number;
    };
    signatures: {
        [filename: string]: string;
    };
    errors: {
        [filename: string]: string;
    };
    static styles: any[];
    constructor();
    private haveCompletedAllSignatures;
    setChecked(event: MouseEvent): void;
    clear(): void;
    renderSelectedFiles(): "" | import("lit-html").TemplateResult<1>;
    render(): import("lit-html").TemplateResult<1>;
    handleFileChanges(event: InputEvent): void;
}
declare global {
    interface HTMLElementTagNameMap {
        'mgnify-sourmash-component': MGnifySourmash;
    }
}
