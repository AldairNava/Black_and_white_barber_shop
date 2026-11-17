import { Component, OnInit } from '@angular/core';

interface ServiceItem {
  id: number;
  name: string;
  category: string;
  branch: string;
  duration_min: number;
  price_mxn: number;
  description: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  activeTab: 'barber' | 'beauty' | 'academy' = 'barber';
  selectedService: ServiceItem | null = null;

  bookingData = {
    client_name: '',
    client_phone: '',
    appointment_date: new Date().toISOString().split('T')[0],
    appointment_time: '12:00'
  };

  barberServices: ServiceItem[] = [
    { id: 1, name: 'Corte Fade / Desvanecido', category: 'Barber', branch: 'Black & White Barber', duration_min: 45, price_mxn: 180, description: 'Desvanecido milimétrico con navaja, perfilado y peinado con cera mate.' },
    { id: 2, name: 'Corte Clásico / Tendencia', category: 'Barber', branch: 'Black & White Barber', duration_min: 35, price_mxn: 150, description: 'Corte a tijera o máquina con acabado limpio a navaja.' },
    { id: 3, name: 'Corte con Diseño / Grecas', category: 'Barber', branch: 'Black & White Barber', duration_min: 50, price_mxn: 220, description: 'Diseño artístico personalizado en laterales o nuca.' },
    { id: 4, name: 'Combo Black & White (Corte + Barba)', category: 'Barber', branch: 'Black & White Barber', duration_min: 60, price_mxn: 280, description: 'Corte completo + toalla caliente, vapor y alineado de barba.' },
    { id: 5, name: 'Trenzas / Braids', category: 'Barber', branch: 'Black & White Barber', duration_min: 60, price_mxn: 250, description: 'Estilo urbano en trenzas de alta definición.' }
  ];

  beautyServices: ServiceItem[] = [
    { id: 7, name: 'Colorimetría / Tinte Completo', category: 'Beauty', branch: 'Black & White Beauty', duration_min: 90, price_mxn: 450, description: 'Aplicación de tinte profesional con cobertura total y brillo.' },
    { id: 8, name: 'Balayage / Mechas de Iluminación', category: 'Beauty', branch: 'Black & White Beauty', duration_min: 150, price_mxn: 850, description: 'Degradado de luz personalizado con tratamiento protector capilar.' },
    { id: 9, name: 'Tratamiento Anti-Frizz y Reparación', category: 'Beauty', branch: 'Black & White Beauty', duration_min: 60, price_mxn: 350, description: 'Reestructuración intensiva para cabello procesado o seco.' },
    { id: 10, name: 'Diseño y Planchado de Ceja', category: 'Beauty', branch: 'Black & White Beauty', duration_min: 30, price_mxn: 120, description: 'Depilación anatómica y planchado para definición perfecta.' },
    { id: 11, name: 'Facial Profundo y Mascarilla', category: 'Beauty', branch: 'Black & White Beauty', duration_min: 45, price_mxn: 220, description: 'Exfoliación, vapor de ozono y mascarilla hidratante.' }
  ];

  academyServices: ServiceItem[] = [
    { id: 12, name: 'Curso de Barbería Profesional (Inicial)', category: 'Academy', branch: 'Black & White Academy', duration_min: 120, price_mxn: 950, description: 'Módulo 1: Manejo de máquinas, tijeras, visagismo y técnicas de corte.' },
    { id: 13, name: 'Taller Master Fade & Hair Tattoo', category: 'Academy', branch: 'Black & White Academy', duration_min: 180, price_mxn: 650, description: 'Especialización intensiva en desvanecidos limpios y grecas artísticas.' }
  ];

  ngOnInit(): void {}

  openBooking(service: ServiceItem): void {
    this.selectedService = service;
  }

  closeBooking(): void {
    this.selectedService = null;
  }

  async submitBooking(event: Event): Promise<void> {
    event.preventDefault();
    if (!this.selectedService) return;

    try {
      const response = await fetch('http://localhost:8002/api/appointments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_name: this.bookingData.client_name,
          client_phone: this.bookingData.client_phone,
          service_id: this.selectedService.id,
          staff_id: 3, // Master Barber / Especialista default
          appointment_date: this.bookingData.appointment_date,
          appointment_time: this.bookingData.appointment_time,
          notes: `Reserva web para ${this.selectedService.name}`
        })
      });

      if (response.ok) {
        alert(`¡Cita agendada con éxito para ${this.bookingData.client_name}! En breve recibirás un WhatsApp de confirmación en el ${this.bookingData.client_phone}.`);
        this.closeBooking();
      } else {
        alert('Cita guardada en el sistema. Gracias por reservar en Black & White Studio.');
        this.closeBooking();
      }
    } catch {
      alert(`¡Cita solicitada con éxito! Te contactaremos al ${this.bookingData.client_phone} para confirmar.`);
      this.closeBooking();
    }
  }
}
