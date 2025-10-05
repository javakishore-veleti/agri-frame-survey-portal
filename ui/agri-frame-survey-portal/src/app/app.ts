import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {HeaderComponent} from '@shared/components/header/header';

@Component({
  selector: 'af-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('agri-frame-survey-portal');
}
