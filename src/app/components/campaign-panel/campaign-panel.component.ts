import {Component, inject, OnDestroy, OnInit} from '@angular/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatTableModule} from '@angular/material/table';
import {Campaign} from '../../data/campaign.data';
import {Subscription} from 'rxjs';
import {HttpService} from '../../services/http.service';
import {CommonModule} from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import {MailViewerDialogComponent} from '../mail-viewer-dialog/mail-viewer-dialog.component';
import {MatDialog} from '@angular/material/dialog';

@Component({
  selector: 'app-campaign-panel',
  imports: [CommonModule, MatExpansionModule, MatIconModule, MatTableModule, MatButtonModule, MailViewerDialogComponent],
  templateUrl: './campaign-panel.component.html',
  styleUrl: './campaign-panel.component.css'
})
export class CampaignPanelComponent implements OnInit, OnDestroy {

  displayedColumns: string[] = ['campaign', 'variant', 'mail', 'recipients', 'clicks', 'purchases'];
  dataSource: Campaign[] = [];

  readonly dialog = inject(MatDialog);


  private subscriptions: Subscription[] = [];


  constructor(private httpService: HttpService) {}

  public ngOnInit() {
    this.subscriptions.push(this.httpService.getAllCampaigns()
      .subscribe(campaigns => {
        this.dataSource = campaigns;
        this.sortDataSource();
      }));

    this.subscriptions.push(this.httpService.getCampaignsGeneratedAsObservable()
      .subscribe((campaigns) => {
        this.dataSource = this.dataSource.concat(campaigns);
        this.sortDataSource();
      }));
  }

  private sortDataSource() {
    this.dataSource.sort((a, b) => {
      const nameCompare = a.name.localeCompare(b.name);
      if (nameCompare !== 0) {
        return nameCompare;
      }
      return a.variant.localeCompare(b.variant);
    });
  }

  public openCampaignMail(campaign: Campaign) {
    this.dialog.open(MailViewerDialogComponent, { data: {campaign}});

  }
  public ngOnDestroy() {
    this.subscriptions.forEach(s => s.unsubscribe());
  }
}
