import React from 'react'

export function Hero({ title = 'Design inspired by Dribbble', subtitle = 'A demo gallery layout for integrating design elements into your healthcare agent application.', cta = 'Get started' }) {
  return (
    <section className="bg-gradient-to-r from-indigo-500 to-pink-500 rounded-xl p-8 text-white">
      <div className="md:flex md:items-center md:justify-between">
        <div>
          <h2 className="text-4xl font-extrabold">{title}</h2>
          <p className="mt-4 text-lg max-w-2xl">{subtitle}</p>
        </div>
        <div className="mt-6 md:mt-0">
          <button className="inline-flex items-center px-4 py-2 bg-white text-indigo-600 rounded-md font-medium shadow-sm">{cta}</button>
        </div>
      </div>
    </section>
  )
}

export function Card({ img, title, desc, assets }) {
  return (
    <article className="bg-white rounded-lg shadow overflow-hidden">
      <img className="w-full h-48 object-cover" src={img} alt={title} />
      <div className="p-4">
        <h4 className="font-semibold text-lg text-gray-900">{title}</h4>
        <p className="mt-2 text-sm text-gray-600">{desc}</p>
        <div className="mt-4 flex items-center justify-between">
          <div className="text-sm text-gray-500">{assets} assets</div>
          <button className="text-indigo-600 font-medium">View</button>
        </div>
      </div>
    </article>
  )
}

export default function Gallery({ items = [] }) {
  return (
    <div>
      <h3 className="text-2xl font-semibold text-gray-900 mb-4">Gallery</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((it, i) => (
          <Card
            key={i}
            img={it.img || `https://source.unsplash.com/collection/190727/800x600?sig=${i}`}
            title={it.title || `Design Card ${i + 1}`}
            desc={it.desc || 'Mockup image and short description'}
            assets={it.assets || 5}
          />
        ))}
      </div>
    </div>
  )
}