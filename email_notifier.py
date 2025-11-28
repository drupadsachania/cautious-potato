"""Email Notifier using Mailgun"""
import requests
from config import Config

class EmailNotifier:
    """Send email alerts via Mailgun"""
    
    def __init__(self):
        self.api_key = Config.MAILGUN_API_KEY
        self.domain = Config.MAILGUN_DOMAIN
        self.endpoint = f"https://api.mailgun.net/v3/{self.domain}/messages"
    
    def send_alert(self, to_email, search_input, results):
        """Send threat alert email"""
        
        # Build email content
        subject = f"🔴 OSINT Alert: Threats Detected for {search_input}"
        
        html_body = self._build_html_report(search_input, results)
        text_body = self._build_text_report(search_input, results)
        
        # Send via Mailgun
        try:
            response = requests.post(
                self.endpoint,
                auth=('api', self.api_key),
                data={
                    'from': f"OSINT Monitor <{Config.NOTIFICATION_EMAIL}>",
                    'to': to_email,
                    'subject': subject,
                    'text': text_body,
                    'html': html_body
                }
            )
            
            if response.status_code == 200:
                return {'status': 'sent', 'message_id': response.json().get('id')}
            else:
                return {'status': 'failed', 'error': response.text}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _build_html_report(self, search_input, results):
        """Build HTML email report"""
        
        threat_count = 0
        threat_items = []
        
        # Count threats
        if results.get('breach'):
            if results['breach'].get('credentials_found'):
                threat_count += 1
                threat_items.append(f"""
                    <li style="margin: 10px 0;">
                        <strong>Breach Found:</strong> {results['breach'].get('breach_count', 0)} breaches
                    </li>
                """)
        
        if results.get('threat'):
            if results['threat'].get('threat_found'):
                threat_count += 1
                threat_items.append(f"""
                    <li style="margin: 10px 0;">
                        <strong>Malicious URL/Domain Detected</strong>
                    </li>
                """)
        
        if results.get('ttp_analysis'):
            ttp = results['ttp_analysis']
            if ttp.get('identified_ttps'):
                threat_count += 1
                threat_items.append(f"""
                    <li style="margin: 10px 0;">
                        <strong>TTPs Identified:</strong> {len(ttp['identified_ttps'])} patterns
                    </li>
                """)
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
                .header {{ background: #d32f2f; color: white; padding: 20px; border-radius: 4px; text-align: center; }}
                .threat-level {{ font-size: 32px; font-weight: bold; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #d32f2f; }}
                .section-title {{ font-size: 18px; font-weight: bold; color: #333; }}
                .details {{ font-size: 14px; line-height: 1.6; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="threat-level">⚠️ THREAT ALERT</div>
                    <p>Potential threats detected during OSINT scan</p>
                </div>
                
                <div class="section">
                    <div class="section-title">🔍 Search Target</div>
                    <div class="details">{search_input}</div>
                </div>
                
                <div class="section">
                    <div class="section-title">🎯 Findings Summary</div>
                    <div class="details">
                        <strong>Threats Found:</strong> {threat_count}
                        <ul style="list-style: none; padding: 0;">
                            {''.join(threat_items) if threat_items else '<li>No immediate threats detected</li>'}
                        </ul>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">📋 Modules Scanned</div>
                    <div class="details">
                        {', '.join(results.get('modules_run', []))}
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from OSINT Monitor</p>
                    <p>Timestamp: {results.get('timestamp', 'N/A')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_text_report(self, search_input, results):
        """Build plain text email report"""
        
        report = f"""
OSINT MONITORING ALERT
========================

Search Target: {search_input}
Modules Scanned: {', '.join(results.get('modules_run', []))}
Timestamp: {results.get('timestamp', 'N/A')}

FINDINGS
--------
"""
        
        if results.get('breach') and results['breach'].get('credentials_found'):
            report += f"\n✓ BREACH DETECTED\n"
            report += f"  Breaches: {results['breach'].get('breach_count', 0)}\n"
        
        if results.get('threat') and results['threat'].get('threat_found'):
            report += f"\n✓ MALICIOUS URL/DOMAIN\n"
        
        if results.get('ttp_analysis') and results['ttp_analysis'].get('identified_ttps'):
            report += f"\n✓ ATTACK PATTERNS IDENTIFIED\n"
            report += f"  TTPs: {len(results['ttp_analysis']['identified_ttps'])}\n"
        
        report += f"""

RECOMMENDATIONS
---------------
1. Review full report in the OSINT Monitor dashboard
2. Take appropriate action based on findings
3. Update security policies if necessary
4. Archive this alert for record-keeping

---
OSINT Monitor v1.0
"""
        
        return report
