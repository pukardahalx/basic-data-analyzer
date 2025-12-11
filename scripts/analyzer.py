import pandas as pd
import matplotlib.pyplot as plt
import os

class SimpleNepalAnalyzer:
    def __init__(self):
        self.base = os.path.dirname(os.path.dirname(__file__))
        self.data_path = os.path.join(self.base, 'data')
        self.output_path = os.path.join(self.base, 'outputs')
        os.makedirs(self.output_path, exist_ok=True)
        
        self.earthquake_data = None
        self.temperature_data = None
        self.exam_data = None
    
    def load_data(self):
        print("Loading Nepalese data...")
        
        earthquake_file = os.path.join(self.data_path, 'earthquakes.csv')
        self.earthquake_data = pd.read_csv(earthquake_file)
        print(f"Earthquakes: {len(self.earthquake_data)} records")
        
        temperature_file = os.path.join(self.data_path, 'temperature.csv')
        self.temperature_data = pd.read_csv(temperature_file)
        print(f"Temperature: {len(self.temperature_data)} months")
        
        exam_file = os.path.join(self.data_path, 'exams.csv')
        self.exam_data = pd.read_csv(exam_file)
        print(f"Exams: {len(self.exam_data)} schools")
    
    def analyze_earthquakes(self):
        print("\nEARTHQUAKE ANALYSIS")
        print("===================")
        
        total_quakes = len(self.earthquake_data)
        avg_magnitude = self.earthquake_data['magnitude'].mean()
        max_magnitude = self.earthquake_data['magnitude'].max()
        total_deaths = self.earthquake_data['deaths'].sum()
        
        print(f"Total Earthquakes: {total_quakes}")
        print(f"Average Magnitude: {avg_magnitude:.2f}")
        print(f"Maximum Magnitude: {max_magnitude}")
        print(f"Total Deaths: {total_deaths}")
        
        year_counts = self.earthquake_data['year'].value_counts().sort_index()
        
        plt.figure(figsize=(10, 6))
        plt.bar(year_counts.index.astype(str), year_counts.values, color='red')
        plt.title('Earthquakes by Year in Nepal')
        plt.xlabel('Year')
        plt.ylabel('Number of Earthquakes')
        
        earthquake_chart = os.path.join(self.output_path, 'earthquake_chart.png')
        plt.savefig(earthquake_chart)
        plt.close()
        
        stats = pd.DataFrame({
            'metric': ['Total Earthquakes', 'Average Magnitude', 'Max Magnitude', 'Total Deaths'],
            'value': [total_quakes, avg_magnitude, max_magnitude, total_deaths]
        })
        
        stats_file = os.path.join(self.output_path, 'earthquake_stats.csv')
        stats.to_csv(stats_file, index=False)
        
        print(f"Chart saved: {earthquake_chart}")
        print(f"Stats saved: {stats_file}")
        
        return stats
    
    def analyze_temperature(self):
        print("\nTEMPERATURE ANALYSIS")
        print("====================")
        
        kathmandu_avg = self.temperature_data['kathmandu'].mean()
        pokhara_avg = self.temperature_data['pokhara'].mean()
        kathmandu_max = self.temperature_data['kathmandu'].max()
        pokhara_max = self.temperature_data['pokhara'].max()
        hottest_month_kath = self.temperature_data.loc[self.temperature_data['kathmandu'].idxmax(), 'month']
        hottest_month_pok = self.temperature_data.loc[self.temperature_data['pokhara'].idxmax(), 'month']
        
        print(f"Kathmandu Average: {kathmandu_avg:.1f}°C")
        print(f"Pokhara Average: {pokhara_avg:.1f}°C")
        print(f"Kathmandu Maximum: {kathmandu_max:.1f}°C in {hottest_month_kath}")
        print(f"Pokhara Maximum: {pokhara_max:.1f}°C in {hottest_month_pok}")
        
        plt.figure(figsize=(10, 6))
        
        plt.plot(self.temperature_data['month'], self.temperature_data['kathmandu'], 
                marker='o', label='Kathmandu', linewidth=2)
        plt.plot(self.temperature_data['month'], self.temperature_data['pokhara'], 
                marker='s', label='Pokhara', linewidth=2)
        
        plt.title('Monthly Temperature in Nepal')
        plt.xlabel('Month')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        temp_chart = os.path.join(self.output_path, 'temperature_chart.png')
        plt.savefig(temp_chart)
        plt.close()
        
        stats = pd.DataFrame({
            'city': ['Kathmandu', 'Pokhara'],
            'average_temp': [kathmandu_avg, pokhara_avg],
            'max_temp': [kathmandu_max, pokhara_max]
        })
        
        stats_file = os.path.join(self.output_path, 'temperature_stats.csv')
        stats.to_csv(stats_file, index=False)
        
        print(f"Chart saved: {temp_chart}")
        print(f"Stats saved: {stats_file}")
        
        return stats
    
    def analyze_exams(self):
        print("\nEXAM ANALYSIS")
        print("=============")
        
        total_students = self.exam_data['students'].sum()
        avg_pass_rate = self.exam_data['pass_percent'].mean()
        best_district = self.exam_data.groupby('district')['pass_percent'].mean().idxmax()
        best_rate = self.exam_data.groupby('district')['pass_percent'].mean().max()
        
        print(f"Total Students: {total_students}")
        print(f"Average Pass Rate: {avg_pass_rate:.1f}%")
        print(f"Best District: {best_district} ({best_rate:.1f}%)")
        
        district_stats = self.exam_data.groupby('district').agg({
            'pass_percent': 'mean',
            'students': 'sum'
        }).reset_index()
        
        plt.figure(figsize=(10, 6))
        
        bars = plt.bar(district_stats['district'], district_stats['pass_percent'], 
                      color=['blue', 'green', 'red', 'purple', 'orange', 'brown'])
        
        plt.title('Pass Percentage by District in Nepal')
        plt.xlabel('District')
        plt.ylabel('Pass Percentage (%)')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        exam_chart = os.path.join(self.output_path, 'exam_chart.png')
        plt.savefig(exam_chart)
        plt.close()
        
        stats_file = os.path.join(self.output_path, 'exam_stats.csv')
        district_stats.to_csv(stats_file, index=False)
        
        print(f"Chart saved: {exam_chart}")
        print(f"Stats saved: {stats_file}")
        
        return district_stats
    
    def create_summary_report(self):
        print("\n" + "="*50)
        print("SUMMARY REPORT")
        print("="*50)
        
        report_lines = []
        report_lines.append("NEPALESE DATA ANALYSIS REPORT")
        report_lines.append("Generated by Simple Nepal Analyzer")
        report_lines.append("="*50)
        
        if self.earthquake_data is not None:
            total_quakes = len(self.earthquake_data)
            avg_mag = self.earthquake_data['magnitude'].mean()
            total_deaths = self.earthquake_data['deaths'].sum()
            
            report_lines.append("EARTHQUAKE DATA:")
            report_lines.append(f"- Total earthquakes: {total_quakes}")
            report_lines.append(f"- Average magnitude: {avg_mag:.2f}")
            report_lines.append(f"- Total deaths: {total_deaths}")
            report_lines.append("")
        
        if self.temperature_data is not None:
            kath_avg = self.temperature_data['kathmandu'].mean()
            pok_avg = self.temperature_data['pokhara'].mean()
            
            report_lines.append("TEMPERATURE DATA:")
            report_lines.append(f"- Kathmandu average: {kath_avg:.1f}°C")
            report_lines.append(f"- Pokhara average: {pok_avg:.1f}°C")
            report_lines.append("")
        
        if self.exam_data is not None:
            total_students = self.exam_data['students'].sum()
            avg_pass = self.exam_data['pass_percent'].mean()
            
            report_lines.append("EXAM DATA:")
            report_lines.append(f"- Total students: {total_students}")
            report_lines.append(f"- Average pass rate: {avg_pass:.1f}%")
            report_lines.append("")
        
        report_lines.append("FILES GENERATED:")
        report_lines.append("- earthquake_chart.png")
        report_lines.append("- temperature_chart.png")
        report_lines.append("- exam_chart.png")
        report_lines.append("- earthquake_stats.csv")
        report_lines.append("- temperature_stats.csv")
        report_lines.append("- exam_stats.csv")
        report_lines.append("")
        report_lines.append("Check the 'outputs' folder!")
        
        report_content = "\n".join(report_lines)
        
        print(report_content)
        
        report_file = os.path.join(self.output_path, 'analysis_report.txt')
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"\nFull report saved: {report_file}")
    
    def run_all(self):
        print("="*50)
        print("SIMPLE NEPALESE DATA ANALYZER")
        print("="*50)
        
        self.load_data()
        
        self.analyze_earthquakes()
        self.analyze_temperature()
        self.analyze_exams()
        
        self.create_summary_report()
        
        print("\n" + "="*50)
        print("ANALYSIS COMPLETE!")
        print("="*50)
        print("Check the 'outputs' folder for charts and data.")

def main():
    analyzer = SimpleNepalAnalyzer()
    analyzer.run_all()

if __name__ == "__main__":
    main()