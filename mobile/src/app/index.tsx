import { useRef, useState } from 'react';
import { AccessibilityInfo, ActivityIndicator, Keyboard, KeyboardAvoidingView, Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { registerCitizen } from '@/services/registration';

type Field = 'nombre' | 'correo' | 'contrasena' | 'confirmacion';
const labels: Record<Field, string> = { nombre: 'Nombre completo', correo: 'Correo electrónico', contrasena: 'Contraseña', confirmacion: 'Confirmar contraseña' };

export default function RegistrationScreen() {
  const [values, setValues] = useState<Record<Field, string>>({ nombre: '', correo: '', contrasena: '', confirmacion: '' });
  const [errors, setErrors] = useState<Partial<Record<Field, string>>>({});
  const [message, setMessage] = useState('');
  const [success, setSuccess] = useState(false);
  const [busy, setBusy] = useState(false);
  const [focused, setFocused] = useState<Field | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const sending = useRef(false);
  const inputs = useRef<Partial<Record<Field, TextInput | null>>>({});

  async function submit() {
    if (sending.current) return;
    const next: Partial<Record<Field, string>> = {};
    if (values.nombre.trim().length < 2 || values.nombre.trim().length > 120) next.nombre = 'Escribe entre 2 y 120 caracteres.';
    if (values.correo.trim().length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.correo.trim())) next.correo = 'Escribe un correo válido.';
    if (values.contrasena.length < 12 || values.contrasena.length > 128) next.contrasena = 'Usa entre 12 y 128 caracteres.';
    if (values.confirmacion !== values.contrasena) next.confirmacion = 'Las contraseñas deben coincidir.';
    setErrors(next);
    setMessage('');
    const first = (Object.keys(labels) as Field[]).find((field) => next[field]);
    if (first) {
      inputs.current[first]?.focus();
      AccessibilityInfo.announceForAccessibility(`${labels[first]}: ${next[first]}`);
      return;
    }
    sending.current = true;
    setBusy(true);
    try {
      await registerCitizen({ nombre: values.nombre.trim(), correo: values.correo.trim().toLowerCase(), contrasena: values.contrasena });
      Keyboard.dismiss();
      setValues({ nombre: '', correo: '', contrasena: '', confirmacion: '' });
      setShowPassword(false);
      setSuccess(true);
      setMessage('Tu cuenta de ciudadano fue creada correctamente. No se ha iniciado sesión.');
      AccessibilityInfo.announceForAccessibility('Tu cuenta de ciudadano fue creada correctamente. No se ha iniciado sesión.');
    } catch (error) {
      const text = error instanceof Error ? error.message : 'No pudimos completar el registro. Intenta de nuevo.';
      setMessage(text);
      AccessibilityInfo.announceForAccessibility(text);
    } finally { sending.current = false; setBusy(false); }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.header}>
        <View style={styles.brandRow} accessible accessibilityLabel="SGIP, Sistema de Gestión de Incidencias en Pereira">
          <View style={styles.logo}><Text style={styles.logoText}>↗</Text></View>
          <Text style={styles.brand}>SGIP</Text>
        </View>
        <Text style={styles.headerCaption}>Pereira</Text>
      </View>
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
        <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag">
          <View style={styles.card}>
            <View style={styles.mode}><Text style={styles.modeText}>Crear cuenta</Text></View>
            <Text style={styles.eyebrow}>PARTICIPACIÓN CIUDADANA</Text>
            <Text accessibilityRole="header" style={styles.title}>{success ? 'Tu cuenta está lista' : 'Crea tu cuenta'}</Text>
            {success ? <>
              <Text accessibilityLiveRegion="polite" style={styles.message}>{message}</Text>
              <Pressable accessibilityRole="button" style={({ pressed }) => [styles.button, pressed && styles.buttonPressed]} onPress={() => { setSuccess(false); setMessage(''); }}><Text style={styles.buttonText}>Registrar otra cuenta</Text></Pressable>
            </> : <>
              <Text style={styles.intro}>Regístrate para reportar y seguir tus casos.</Text>
              <Text style={styles.required}>Todos los campos son obligatorios (*).</Text>
              {(Object.keys(labels) as Field[]).map((field, index, fields) => (
                <View key={field} style={styles.field}>
                  <Text nativeID={`${field}-label`} style={styles.label}>{labels[field]} *</Text>
                  <View style={styles.inputRow}>
                  <TextInput
                    ref={(input) => { inputs.current[field] = input; }}
                    accessibilityLabel={`${labels[field]}, obligatorio${errors[field] ? `. ${errors[field]}` : ''}`}
                    accessibilityHint={field === 'contrasena' ? 'Entre 12 y 128 caracteres, sin eliminar espacios.' : undefined}
                    style={[styles.input, focused === field && styles.focused, errors[field] && styles.invalid]}
                    onFocus={() => setFocused(field)}
                    onBlur={() => setFocused(null)}
                    value={values[field]}
                    onChangeText={(text) => { setValues((current) => ({ ...current, [field]: text })); setErrors((current) => ({ ...current, [field]: undefined })); setMessage(''); }}
                    editable={!busy} autoCapitalize={field === 'nombre' ? 'words' : 'none'} autoCorrect={false}
                    keyboardType={field === 'correo' ? 'email-address' : 'default'}
                    secureTextEntry={(field === 'contrasena' && !showPassword) || field === 'confirmacion'}
                    underlineColorAndroid="transparent"
                    autoComplete={field === 'nombre' ? 'name' : field === 'correo' ? 'email' : 'new-password'}
                    returnKeyType={field === 'confirmacion' ? 'done' : 'next'}
                    submitBehavior={field === 'confirmacion' ? 'blurAndSubmit' : 'submit'}
                    onSubmitEditing={() => field === 'confirmacion' ? void submit() : inputs.current[fields[index + 1]]?.focus()}
                  />
                  {field === 'contrasena' && <Pressable
                    accessibilityRole="button"
                    accessibilityLabel={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                    accessibilityState={{ disabled: busy }}
                    disabled={busy}
                    onPress={() => setShowPassword((current) => !current)}
                    style={({ pressed }) => [styles.reveal, pressed && styles.revealPressed, busy && styles.disabled]}>
                    <Text style={styles.revealText}>{showPassword ? 'Ocultar' : 'Mostrar'}</Text>
                  </Pressable>}
                  </View>
                  {field === 'contrasena' && <Text style={styles.hint}>Entre 12 y 128 caracteres. Se conservan los espacios.</Text>}
                  {errors[field] && <Text accessibilityLiveRegion="polite" style={styles.error}>{errors[field]}</Text>}
                </View>
              ))}
              {!!message && <Text accessibilityRole="alert" accessibilityLiveRegion="assertive" style={styles.errorNotice}>{message}</Text>}
              <Pressable accessibilityRole="button" accessibilityState={{ disabled: busy, busy }} disabled={busy} style={({ pressed }) => [styles.button, pressed && styles.buttonPressed, busy && styles.disabled]} onPress={() => void submit()}>
                {busy && <ActivityIndicator color="#fff" />}<Text style={styles.buttonText}>{busy ? 'Creando cuenta…' : 'Crear mi cuenta'}</Text>
              </Pressable>
              <Text style={styles.footerHint}>Si falla la conexión, tus datos se conservan para que puedas volver a intentar.</Text>
            </>}
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#f3f5f0' }, flex: { flex: 1 },
  header: { paddingHorizontal: 20, paddingVertical: 16, backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#dce4dc', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  brandRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  logo: { width: 36, height: 36, borderRadius: 12, backgroundColor: '#d8ec91', alignItems: 'center', justifyContent: 'center' },
  logoText: { color: '#173d35', fontSize: 24 }, brand: { color: '#173d35', fontSize: 22, fontWeight: '800', letterSpacing: -1 },
  headerCaption: { color: '#60736d', fontSize: 13 },
  content: { flexGrow: 1, paddingHorizontal: 25, paddingTop: 29, paddingBottom: 32, alignItems: 'center' },
  card: { width: '100%', maxWidth: 490 },
  mode: { alignSelf: 'flex-start', minHeight: 44, justifyContent: 'center', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 9, backgroundColor: '#173d35', marginBottom: 20 },
  modeText: { color: '#fff', fontSize: 15, fontWeight: '600' },
  eyebrow: { color: '#17634e', fontSize: 11, fontWeight: '700', letterSpacing: 1.7, marginBottom: 8 },
  title: { color: '#173d35', fontSize: 26, lineHeight: 32, letterSpacing: -1, fontWeight: '700', marginBottom: 12 },
  intro: { color: '#60736d', fontSize: 15, lineHeight: 23, marginBottom: 12 },
  required: { color: '#60736d', fontSize: 12, lineHeight: 18, marginBottom: 15 },
  field: { marginBottom: 15 }, label: { color: '#173d35', fontWeight: '600', fontSize: 13, lineHeight: 20, marginBottom: 7 },
  inputRow: { flexDirection: 'row', alignItems: 'stretch', gap: 12 },
  input: { flex: 1, minWidth: 0, minHeight: 46, borderWidth: 1, borderColor: '#bccac0', borderRadius: 8, paddingHorizontal: 12, paddingVertical: 11, color: '#173d35', backgroundColor: '#fff', fontSize: 16 },
  focused: { borderColor: '#a05c09', outlineColor: '#a05c09', outlineWidth: 2, outlineOffset: 2 },
  invalid: { borderColor: '#a43833', borderWidth: 2 }, hint: { color: '#60736d', fontSize: 12, lineHeight: 18, marginTop: 5 },
  error: { color: '#a43833', fontSize: 13, lineHeight: 20, marginTop: 5 },
  errorNotice: { color: '#a43833', fontSize: 13, lineHeight: 20, padding: 14, backgroundColor: '#fce8e4', borderColor: '#a43833', borderWidth: 1, borderRadius: 10, marginBottom: 18 },
  message: { color: '#246344', fontSize: 15, lineHeight: 23, padding: 16, backgroundColor: '#f1f6e6', borderColor: '#dce5c6', borderWidth: 1, borderRadius: 10, marginBottom: 18 },
  button: { minHeight: 48, paddingHorizontal: 16, paddingVertical: 12, borderRadius: 9, backgroundColor: '#17634e', alignItems: 'center', justifyContent: 'center', flexDirection: 'row', gap: 10 },
  buttonPressed: { backgroundColor: '#104936' }, disabled: { opacity: 0.5 },
  buttonText: { color: '#fff', fontWeight: '600', fontSize: 15, textAlign: 'center' },
  reveal: { minHeight: 46, paddingHorizontal: 12, paddingVertical: 10, borderWidth: 1, borderColor: '#dce4dc', borderRadius: 9, justifyContent: 'center', backgroundColor: '#fff' },
  revealPressed: { backgroundColor: '#edf3e9' }, revealText: { color: '#173d35', fontSize: 14, fontWeight: '600' },
  footerHint: { color: '#60736d', fontSize: 12, lineHeight: 18, marginTop: 20 },
});
