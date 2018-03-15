export const isInStore = (messageId) => {
  const storage = localStorage.getItem('prodeko_tiedotteet')
  if (storage === null) {
    return false
  }
  const messages = storage.split(',')
  if (messages.includes(messageId.toString())) {
    return true
  }
  return false;
}

export const addToStorage = (messageId) => {
  const storage = localStorage.getItem('prodeko_tiedotteet')
  if (storage === null) {
    localStorage.setItem('prodeko_tiedotteet', [])
  }
  if (!isInStore(messageId)) {
    const messages = storage.split(',')
    localStorage.setItem('prodeko_tiedotteet', [...messages, messageId])
  }
}

export const removeFromStorage = (messageId) => {
  const storage = localStorage.getItem('prodeko_tiedotteet')
  if (storage === null) {
    return false
  }
  if (isInStore(messageId)) {
    const messages = storage.split(',')
    localStorage.setItem('prodeko_tiedotteet', messages.filter(m => m !== messageId.toString()))
  }
}
