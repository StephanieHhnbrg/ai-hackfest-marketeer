import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import {provideHttpClient} from '@angular/common/http';
import {provideNativeDateAdapter} from '@angular/material/core';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(),
    provideNativeDateAdapter(),
  ]
};
