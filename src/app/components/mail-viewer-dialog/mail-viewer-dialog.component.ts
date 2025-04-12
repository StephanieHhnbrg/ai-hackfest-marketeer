import {Component, Inject, OnInit} from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogContent,
  MatDialogTitle
} from '@angular/material/dialog';
import {Campaign} from '../../data/campaign.data';
import {MatButtonModule} from '@angular/material/button';
import {DomSanitizer, SafeHtml} from '@angular/platform-browser';

@Component({
  selector: 'app-mail-viewer-dialog',
  imports: [
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent],
  templateUrl: './mail-viewer-dialog.component.html',
  styleUrl: './mail-viewer-dialog.component.css'
})
export class MailViewerDialogComponent implements OnInit {

  public subjectLine = "";
  public mailBody: SafeHtml = "";

  constructor(private sanitized: DomSanitizer,
              @Inject(MAT_DIALOG_DATA) public data: { campaign: Campaign }) {
  }

  ngOnInit() {
    this.subjectLine = this.data.campaign.subjectLine;
    let content = this.data.campaign.content
      .replace("<!DOCTYPE html><html><head></head><body>", "")
      .replace("</body></html>","")
      .replace("<USER-NAME>","[Customer name]");

    this.mailBody = this.sanitized.bypassSecurityTrustHtml(content);
  }
}
