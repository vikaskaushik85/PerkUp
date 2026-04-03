import React from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';

interface Props {
  size?: number;
  color?: string;
  showText?: boolean;
  textColor?: string;
}

/**
 * PerkUp logo — renders the app icon image.
 */
export function PerkUpLogo({
  size = 88,
  color = '#D97706',
  showText = false,
  textColor,
}: Props) {
  return (
    <View style={showText ? styles.row : undefined}>
      <Image
        source={require('@/assets/images/icon.png')}
        style={{
          width: size,
          height: size,
          borderRadius: size * 0.2,
        }}
      />
      {showText && (
        <Text style={[styles.text, { color: textColor ?? color }]}>PerkUp</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center' },
  text: {
    fontSize: 28,
    fontWeight: 'bold',
    marginLeft: 14,
  },
});
