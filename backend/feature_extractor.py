import re
from urllib.parse import urlparse
import tldextract


class FeatureExtractor:
    def extract_url_features(self, url):
        """Extract features from URL for phishing detection"""
        features = {}

        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)

            # URL length features
            features['url_length'] = len(url)
            features['domain_length'] = len(extracted.domain)
            features['path_length'] = len(parsed.path)

            # Domain features
            features['subdomain_count'] = len(
                extracted.subdomain.split('.')) if extracted.subdomain else 0
            features['has_ip'] = 1 if re.match(
                r'\d+\.\d+\.\d+\.\d+', parsed.netloc) else 0

            # Suspicious characters
            features['dot_count'] = url.count('.')
            features['dash_count'] = url.count('-')
            features['at_symbol'] = 1 if '@' in url else 0
            features['double_slash_redirect'] = 1 if url.count('//') > 1 else 0

            # Protocol features
            features['https'] = 1 if parsed.scheme == 'https' else 0

            # Suspicious keywords
            suspicious_keywords = [
                'login', 'verify', 'account', 'update', 'secure', 'banking', 'confirm']
            features['suspicious_keywords'] = sum(
                1 for kw in suspicious_keywords if kw in url.lower())

            # URL shortening services
            shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly']
            features['is_shortened'] = 1 if any(
                short in url.lower() for short in shorteners) else 0

            # Special characters
            features['special_char_count'] = len(
                re.findall(r'[^a-zA-Z0-9]', url))

            # Digit ratio
            digits = len(re.findall(r'\d', url))
            features['digit_ratio'] = digits / len(url) if len(url) > 0 else 0

        except Exception as e:
            print(f"Error extracting features: {e}")
            # Return default features on error
            features = {k: 0 for k in ['url_length', 'domain_length', 'path_length',
                                       'subdomain_count', 'has_ip', 'dot_count', 'dash_count',
                                       'at_symbol', 'double_slash_redirect', 'https',
                                       'suspicious_keywords', 'is_shortened', 'special_char_count',
                                       'digit_ratio']}

        return features

    def extract_email_features(self, email_content):
        """Extract features from email content"""
        features = {}

        # Email length
        features['email_length'] = len(email_content)

        # Urgency keywords
        urgency_words = ['urgent', 'immediate',
                         'action required', 'verify', 'suspend', 'limited time']
        features['urgency_count'] = sum(
            1 for word in urgency_words if word in email_content.lower())

        # Links in email
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, email_content)
        features['url_count'] = len(urls)

        # Suspicious phrases
        suspicious_phrases = [
            'click here', 'verify your account', 'confirm your identity', 'update payment']
        features['suspicious_phrases'] = sum(
            1 for phrase in suspicious_phrases if phrase in email_content.lower())

        # Exclamation marks (often used in phishing)
        features['exclamation_count'] = email_content.count('!')

        return features
