# Process

## Tools Used

I used ChatGPT as the main AI tool during this project.

It was used to help me understand the assignment requirements, explore different visualisation directions, generate and revise Python code, troubleshoot errors, compare possible data sources, and improve the animation structure.

I treated AI-generated outputs as suggestions rather than final decisions. Some ideas were tested and later rejected when they did not communicate the data clearly or did not match the visual direction I wanted.

For example, I rejected layouts that added too many statistics and decorative elements. I also rejected the suggestion to reduce the number of daily lines because I wanted to preserve all 365 daily observations.

The final visualisation was therefore developed through repeated testing, comparison, and revision rather than by directly using the first AI-generated result.

---

## 1. Choosing the Data

I first chose sunrise and sunset times in Hong Kong as the natural phenomenon for this project.

The data comes from the Hong Kong Observatory and contains one record for each day in 2026.

I was interested in this dataset because the change in daylight is very small from one day to the next, but becomes much more visible when the whole year is viewed together.

My initial goal was to find a visual form that could show this gradual annual change clearly without becoming a conventional statistical chart.

---

## 2. First Line Chart

My first experiment was a simple line chart showing sunrise and sunset across the year.

This version worked as a basic data visualisation because the seasonal pattern could already be seen.

However, the result felt too similar to a conventional statistical chart and did not have a strong visual identity.

I therefore started to explore different ways of transforming the same data.

---

## 3. Circular Visualisation

One early direction was to arrange the 365 days around a circle.

I initially thought this would fit the idea of an annual cycle.

After generating the result, however, I found that the variation in Hong Kong sunrise and sunset times was relatively small. This meant that the circular outline did not change very much.

The structure of the circle became more noticeable than the actual data.

I therefore rejected this direction.

---

## 4. Poster-Style Experiments

I then experimented with more complex poster-style compositions.

These versions included additional statistics, labels, decorative elements, and supporting graphics.

Although they appeared more visually complete, I found that they distracted from the main data.

At this stage, I realised that the visualisation did not need more information. It needed a clearer visual rule.

The key idea that emerged from this stage was:

**one day = one vertical line**

This became the basic visual system of the final project.

---

## 5. Developing the 365-Day Structure

I represented each day as one vertical line.

The upper endpoint of the line represents sunrise, while the lower endpoint represents sunset.

Because of this, the length of each line directly represents the amount of daylight on that day.

When all 365 daily lines are placed next to each other, the gradual expansion and contraction of daylight becomes visible across the year.

At first, the result felt too dense and crowded.

One possible solution was to show only every second or third day. I decided not to use this approach because I wanted every day to remain visible as an individual observation.

Instead, I changed the overall layout.

The visualisation became much wider and more horizontal, giving the 365 lines more space without removing any data.

This became an important design decision in the final version.

---

## 6. Testing Another Dataset

During the project, I temporarily explored a different direction using NASA POWER solar radiation data.

I downloaded regional monthly solar radiation data from 2016 to 2025 and processed it into a spatial dataset.

I created a bivariate map where:

- colour represented mean solar radiation
- circle size represented interannual variability

The transformation worked technically, but the selected region contained only 15 spatial grid points.

As a result, the map felt too sparse for the visual style I was trying to achieve.

I decided not to continue with this direction and returned to the sunrise and sunset dataset.

This experiment helped me realise that a more complex dataset does not automatically produce a stronger visualisation.

---

## 7. Returning to Sunrise and Sunset

After testing the solar radiation dataset, I returned to the sunrise and sunset project.

At this stage, I simplified the composition further.

I removed unnecessary statistics and secondary graphics so that the daily lines became the main visual element.

The final static visualisation is based on three direct mappings:

- horizontal position = date
- upper endpoint = sunrise
- lower endpoint = sunset

The distance between the upper and lower endpoints represents daylight duration.

This simple structure made the seasonal pattern clearer than the earlier versions.

---

## 8. Developing the Colour System

Earlier versions used stronger yellow, orange, and red colours.

I found that these colours made the visualisation feel too similar to a heat map and became too visually dominant.

I wanted colour to support the concept of daylight rather than represent another quantitative variable.

I therefore developed a softer sky-inspired gradient inside each daily line.

The gradient moves from warm sunrise tones, through pale daylight colours, and back towards warmer sunset tones.

These colours are not measured sky-colour data.

They are an artistic interpretation used to reinforce the idea of changing daylight within one day.

The actual Hong Kong Observatory data still determines the position and length of every line.

---

## 9. Refining the Composition

I continued simplifying the final composition.

The title was changed to:

**A Year of Light**

The subtitle identifies the subject as Hong Kong sunrise and sunset data from 2026.

I removed most of the additional statistics and kept only the essential labels such as months, times, title, subtitle, and data source.

This made the visualisation feel more focused and allowed the structure of the 365 daily lines to become the main visual feature.

---

## 10. Adding Animation

After the static visualisation was established, I created a small animated version.

The complete year remains visible in the background while one day is highlighted at a time.

For the highlighted day, the animation displays:

- date
- sunrise time
- sunset time
- daylight duration

The daily information moves together with the highlighted line so that the viewer can connect the numerical values directly to the visual position.

The first animation version was very slow because too many individual line segments were redrawn for every frame.

I later optimised the code so that the full 365-day background is created only once and only the highlighted day is updated during the animation.

This significantly improved the rendering speed.

I kept the animation simple because its purpose is to support the static visualisation rather than become a separate visual effect.

---

## 11. What I Kept

The most important rule I kept was:

**one day = one line**

I kept all 365 observations because I wanted the visualisation to preserve the full temporal structure of the dataset.

I also kept the wide horizontal format because it solved the problem of visual density without removing data.

The soft colour gradient was also retained because it supports the idea of daylight while remaining secondary to the actual data mapping.

---

## 12. What I Rejected

I rejected the circular visualisation because the small annual variation produced a weak circular form.

I rejected the more complex poster layouts because the additional statistics and decorative elements distracted from the main message.

I rejected the NASA POWER solar radiation map because the available spatial resolution produced only 15 grid points in the selected region.

I also rejected the idea of displaying only every second or third day because this would remove the direct relationship between one day and one visual observation.

---

## 13. AI Corrections and Decisions

ChatGPT helped generate and revise parts of the Python code and suggested several possible visual directions.

However, I did not keep every suggestion.

Some generated versions included too many statistics, labels, and decorative elements. I removed them because I wanted the visualisation to communicate one clear relationship.

I also rejected suggestions to reduce the number of daily lines.

The colour palette was revised several times until it became softer and less similar to a conventional heat map.

The animation structure was also changed after the first version was too slow to render.

The final project therefore developed through repeated testing, visual comparison, rejection, and revision rather than directly using the first AI-generated output.