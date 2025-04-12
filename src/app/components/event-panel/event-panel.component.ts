import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatTable, MatTableModule} from '@angular/material/table';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatInputModule} from '@angular/material/input';
import {Subscription} from 'rxjs';
import {HttpService} from '../../services/http.service';
import {CommonModule} from '@angular/common';
import {SalesEvent} from '../../data/event.data';
import {MatButtonModule} from '@angular/material/button';

@Component({
  selector: 'app-event-panel',
  imports: [CommonModule, MatExpansionModule, MatIconModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatDatepickerModule, MatTableModule],
  templateUrl: './event-panel.component.html',
  styleUrl: './event-panel.component.css'
})
export class EventPanelComponent implements OnInit, OnDestroy {

  displayedColumns: string[] = ['date', 'description', 'campaign'];
  dataSource: SalesEvent[] = [];
  @ViewChild(MatTable) table: MatTable<SalesEvent> | undefined;


  private subscriptions: Subscription[] = [];


  constructor(private httpService: HttpService) {}

  public ngOnInit() {
    this.subscriptions.push(this.httpService.getAllEvents()
      .subscribe((events: SalesEvent[]) => {
        this.dataSource = events;
        this.dataSource.sort((a, b) => { return new Date(a.date).getTime() - new Date(b.date).getTime(); });
      }));
  }

  public addEvent(description: string, date: string) {
    if (description.length == 0 || !this.isValidDate(date)) {
      return;
    }
    let event = { description, date, campaigns: [] };
    this.dataSource.push(event);
    this.httpService.registerEvent(event);
    this.table!.renderRows();
  }


  private isValidDate(dateStr: string): boolean {
    const regex = /^(|[1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[12]\d|3[01])\/\d{4}$/;
    if (!regex.test(dateStr)) {
      return false;
    }

    // Check if it's a real date (e.g., not 02/30/2023)
    const [month, day, year] = dateStr.split('/').map(Number);
    const date = new Date(year, month - 1, day);

    return (
      date.getFullYear() === year &&
      date.getMonth() === month - 1 &&
      date.getDate() === day
    ) && date > new Date();
  }
  public ngOnDestroy() {
    this.subscriptions.forEach(s => s.unsubscribe());
  }
}
