import {Component, OnDestroy, OnInit} from '@angular/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatTableModule} from '@angular/material/table';
import {Campaign} from '../../data/campaign.data';
import {Subscription} from 'rxjs';
import {HttpService} from '../../services/http.service';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-campaign-panel',
  imports: [CommonModule, MatExpansionModule, MatIconModule, MatTableModule],
  templateUrl: './campaign-panel.component.html',
  styleUrl: './campaign-panel.component.css'
})
export class CampaignPanelComponent implements OnInit, OnDestroy {

  displayedColumns: string[] = ['campaign', 'variant', 'mail', 'recipients', 'clicks', 'purchases'];
  dataSource: Campaign[] = [];

  private subscriptions: Subscription[] = [];


  constructor(private httpService: HttpService) {}

  public ngOnInit() {
    this.subscriptions.push(this.httpService.getAllCampaigns()
      .subscribe(campaigns => {
        this.dataSource = campaigns;
      }));

    this.subscriptions.push(this.httpService.getCampaignsGeneratedAsObservable()
      .subscribe((campaigns) => {
        this.dataSource = this.dataSource.concat(campaigns);
      }));
  }

  public ngOnDestroy() {
    this.subscriptions.forEach(s => s.unsubscribe());
  }
}
